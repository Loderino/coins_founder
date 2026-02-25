const cache = new Map();
const CACHE_TTL = 5 * 60 * 1000;

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'FETCH_SALES') {
    handleFetchSales(request.data, request.coinId)
      .then(data => sendResponse({ success: true, data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }
});

async function handleFetchSales(data, coinId) {
  if (coinId) {
    const cacheKey = `${coinId}`;
    const cached = cache.get(cacheKey);
    
    if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
      console.log(`📦 Background: возвращаю из кэша монету ${coinId}`);
      return cached.data;
    }
  }

  console.log(`🌐 Background: запрос к API для монеты ${coinId}`);
  
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/sales', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) throw new Error(`API error: ${response.status}`);
    
    const result = await response.json();
    
    if (coinId) {
      const cacheKey = `${coinId}`;
      cache.set(cacheKey, {
        timestamp: Date.now(),
        data: result
      });
      console.log(`💾 Background: сохранено в кэш для монеты ${coinId}`);
    }
    
    cleanupCache();
    
    return result;
  } catch (error) {
    console.error('❌ Background error:', error);
    throw error;
  }
}

function cleanupCache() {
  const now = Date.now();
  for (const [key, value] of cache.entries()) {
    if (now - value.timestamp > CACHE_TTL) {
      cache.delete(key);
      console.log(`🧹 Очищен кэш для ${key}`);
    }
  }
}

// Очистка кэша раз в час
setInterval(cleanupCache, 60 * 60 * 1000);

// Посмотреть содержимое кэша (для отладки)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'GET_CACHE_STATS') {
    const stats = {};
    cache.forEach((value, key) => {
      stats[key] = {
        age: Math.round((Date.now() - value.timestamp) / 1000) + ' сек',
        size: JSON.stringify(value.data).length
      };
    });
    sendResponse(stats);
  }
});