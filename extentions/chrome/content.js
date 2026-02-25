console.log('Content script loaded');

function parseTooltipData(tooltip) {
  const body = tooltip.querySelector('.body');
  if (!body) return null;

  const textNodes = [];
  const walker = document.createTreeWalker(
    body,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode: function(node) {
        if (node.textContent.trim() === '') return NodeFilter.FILTER_REJECT;
        if (node.parentElement.style.display === 'none') return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    }
  );

  while (walker.nextNode()) {
    const text = walker.currentNode.textContent.trim();
    if (text) textNodes.push(text);
  }

  const result = {
    sources: [],
    title: '',
    country: '',
    currency: '',
    nominal: '',
    year: null,
    is_regular: false,
  };
  const searchParams = window.location.search;
  if (!searchParams.type||searchParams.type==1) {
    result.is_regular = true;
  }

  let coin_info = textNodes[0];
  let info = coin_info.split(" ");
  result.country = info.slice(0, info.length - 3).join(" ");
  result.nominal = info.at(-3);
  result.currency = info.at(-2);
  result.year = info.at(-1);

  if (textNodes[1].includes("#")){
    result.title = textNodes[0];
  } else {
    if (textNodes[1].includes("Отметка монетного двора:")){
      result.title = textNodes[0];
      result.mintmark = textNodes[1].split("Отметка монетного двора: ")[1].split(" -")[0].split('"')[1];
    } else {
        if (result.is_regular) result.title = textNodes[0];
        else result.title = textNodes[1];
        if (textNodes[2].includes("Отметка монетного двора:")){
            result.mintmark = textNodes[2].split(" ")[3].split('"')[1];
        }
    }
  }
  return result;
}

function getCoinIdFromLink() {
  const tooltip = document.getElementById('tooltip');
  let body = tooltip.getElementsByClassName("body")[0];
  console.log(body.getElementsByTagName("div"));
  if (body.querySelector("img:last-child")){
      return body.querySelector("img:last-child").attributes["src"].value.split("/")[6].split("-")[0].trim();
  }
  else {
    return body.querySelector("div:last-child").textContent.split("|")[0].trim();    
  }
}

// Отправка запроса через background
async function sendToApi(data) {
  try {
    const { enabledSources } = await chrome.storage.sync.get(['enabledSources']);
    data.sources = enabledSources || [];
    
    const coinId = getCoinIdFromLink();
    console.log(`🔍 Отправка запроса для монеты ${coinId}`);

    console.log(data);
    return new Promise((resolve, reject) => {
      chrome.runtime.sendMessage({
        type: 'FETCH_SALES',
        data: data,
        coinId: coinId
      }, response => {
        if (response.success) {
          console.log(`📥 Получен ответ для монеты ${coinId}`);
          resolve(response.data);
        } else {
          reject(new Error(response.error));
        }
      });
    });
  } catch (error) {
    console.error('❌ Ошибка:', error);
    return null;
  }
}

function displayResults(tooltip, salesData) {
  const oldBlock = tooltip.querySelector('.numis-helper-data');
  if (oldBlock) oldBlock.remove();

  const resultBlock = document.createElement('div');
  resultBlock.className = 'numis-helper-data';
  resultBlock.style.cssText = `
    margin: 8px;
    padding: 10px;
    background: #1e2a3a;
    border-radius: 10px;
    color: #e2e8f0;
    font-size: 11px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    border: 1px solid #334155;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  `;

  let realSalesData = [];
  salesData.forEach(sale => {
    if (sale.min_price){
      realSalesData.push(sale);
    }
  });

  if (!realSalesData || realSalesData.length === 0) {
    resultBlock.innerHTML = `
      <div style="text-align: center; padding: 6px; color: #94a3b8;">
        ⚡ Нет предложений
      </div>
    `;
  } else {
    let html = `
      <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 8px; padding-bottom: 6px; border-bottom: 1px solid #334155;">
        <span style="background: #3b82f6; color: white; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 600;">
          ${realSalesData.length}
        </span>
        <span style="color: #94a3b8;">цены на рынке</span>
      </div>
    `;

    const sortedSources = [...realSalesData].sort((a, b) => a.min_price - b.min_price);
    const icons = ['🪙', '🏪', '📊', '🏛️', '🌐'];

    sortedSources.forEach((source, index) => {
      const icon = icons[index % icons.length];
      
      html += `
        <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 6px; padding: 4px; background: #263340; border-radius: 6px;">
          <span style="width: 16px;">${icon}</span>
          <div style="flex: 1; display: flex; gap: 8px;">
            <span style="color: #4ade80; font-weight: 600; min-width: 40px;">${source.min_price}₽</span>
            <span style="color: #fbbf24; min-width: 40px;">${source.avg_price}₽</span>
            <span style="color: #f87171; min-width: 40px;">${source.max_price}₽</span>
          </div>
          <span style="color: #94a3b8; font-size: 10px;">${source.total_variants}</span>
        </div>
      `;
    });

    const totalMin = Math.min(...realSalesData.map(s => s.min_price));
    const totalMax = Math.max(...realSalesData.map(s => s.max_price));
    
    html += `
      <div style="margin-top: 6px; padding-top: 6px; border-top: 1px solid #334155; display: flex; justify-content: space-between; color: #94a3b8; font-size: 10px;">
        <span>диапазон:</span>
        <span><span style="color: #4ade80;">${totalMin}₽</span> — <span style="color: #f87171;">${totalMax}₽</span></span>
      </div>
    `;

    resultBlock.innerHTML = html;
  }

  tooltip.appendChild(resultBlock);
}

setInterval(() => {
  const tooltip = document.getElementById('tooltip');
  if (!tooltip) return;
  
  if (tooltip.style.display === 'none' && tooltip.querySelector('.numis-helper-data')) {
    tooltip.querySelector('.numis-helper-data').remove();
  }
  
  if (tooltip.style.display === 'block' && !tooltip.querySelector('.numis-helper-data')) {
    const coinData = parseTooltipData(tooltip);
    if (!coinData) return;

    const loadingBlock = document.createElement('div');
    loadingBlock.className = 'numis-helper-data';
    loadingBlock.style.cssText = `
      margin: 8px;
      padding: 8px;
      background: #1e2a3a;
      border-radius: 10px;
      color: #94a3b8;
      font-size: 11px;
      text-align: center;
      border: 1px solid #334155;
    `;
    loadingBlock.innerHTML = '🔍 загрузка...';
    tooltip.appendChild(loadingBlock);

    sendToApi(coinData).then(salesData => {
      loadingBlock.remove();
      displayResults(tooltip, salesData);
    });
  }
}, 300);