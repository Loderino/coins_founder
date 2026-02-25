document.addEventListener('DOMContentLoaded', function() {
  const sourcesContainer = document.getElementById('sources-container');
  const refreshBtn = document.getElementById('refresh-btn');
  const saveBtn = document.getElementById('save-btn');
  const statusMessage = document.getElementById('status-message');

  // Загрузка источников с API
  async function loadSources() {
    sourcesContainer.innerHTML = '<div class="loading">Загрузка источников...</div>';
    
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/sources');
      const data = await response.json();
      
      if (data.sources && Array.isArray(data.sources)) {
        renderSources(data.sources);
        loadSavedState();
      } else {
        throw new Error('Неверный формат данных');
      }
    } catch (error) {
      console.error('Ошибка загрузки источников:', error);
      sourcesContainer.innerHTML = `
        <div class="error" style="text-align: center; padding: 20px; color: #f87171;">
          ❌ Ошибка загрузки источников<br>
          <span style="font-size: 11px;">${error.message}</span>
        </div>
      `;
    }
  }

  function renderSources(sources) {
    sourcesContainer.innerHTML = '';
    
    sources.forEach(source => {
      const sourceItem = document.createElement('div');
      sourceItem.className = 'source-item';
      
      const checkboxDiv = document.createElement('div');
      checkboxDiv.className = 'source-checkbox';
      
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.id = `source-${source.id}`;
      checkbox.dataset.id = source.id;
      
      const label = document.createElement('label');
      label.htmlFor = `source-${source.id}`;
      
      checkboxDiv.appendChild(checkbox);
      checkboxDiv.appendChild(label);
      
      const iconImg = document.createElement('img');
      iconImg.src = source.icon || 'https://via.placeholder.com/16';
      iconImg.alt = '';
      iconImg.style.cssText = `
        width: 20px;
        height: 20px;
        border-radius: 4px;
        object-fit: contain;
      `;
      iconImg.onerror = () => {
        iconImg.src = 'data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'16\' height=\'16\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'%2394a3b8\' stroke-width=\'2\'%3E%3Ccircle cx=\'12\' cy=\'12\' r=\'10\'/%3E%3Cpath d=\'M12 8v8\'/%3E%3Cpath d=\'M8 12h8\'/%3E%3C/svg%3E';
      };
      
      const infoDiv = document.createElement('div');
      infoDiv.className = 'source-info';
      infoDiv.style.cssText = `
        display: flex;
        align-items: center;
        gap: 8px;
        flex: 1;
      `;
      
      infoDiv.appendChild(iconImg);
      
      const nameDiv = document.createElement('div');
      nameDiv.style.cssText = `
        display: flex;
        flex-direction: column;
      `;
      
      const nameSpan = document.createElement('span');
      nameSpan.className = 'source-name';
      nameSpan.textContent = source.id.charAt(0).toUpperCase() + source.id.slice(1).replace('_', ' ');
      
      const badgeDiv = document.createElement('div');
      badgeDiv.className = 'source-badge';
      badgeDiv.textContent = source.badge || 'API';
      badgeDiv.style.cssText = `
        font-size: 10px;
        color: #94a3b8;
      `;
      
      nameDiv.appendChild(nameSpan);
      nameDiv.appendChild(badgeDiv);
      
      infoDiv.appendChild(nameDiv);
      
      const linkIcon = document.createElement('a');
      linkIcon.href = source.link || '#';
      linkIcon.target = '_blank';
      linkIcon.innerHTML = '↗️';
      linkIcon.style.cssText = `
        text-decoration: none;
        color: #94a3b8;
        font-size: 14px;
        padding: 4px;
        border-radius: 4px;
        hover: background: #2d3748;
      `;
      linkIcon.onmouseover = (e) => e.target.style.opacity = '1';
      linkIcon.onmouseout = (e) => e.target.style.opacity = '0.6';
      
      sourceItem.appendChild(checkboxDiv);
      sourceItem.appendChild(infoDiv);
      sourceItem.appendChild(linkIcon);
      
      sourcesContainer.appendChild(sourceItem);
    });
  }

  // Загрузка сохраненного состояния из chrome.storage
  function loadSavedState() {
    chrome.storage.sync.get(['enabledSources'], function(result) {
      if (result.enabledSources) {
        const checkboxes = document.querySelectorAll('.source-checkbox input');
        checkboxes.forEach(checkbox => {
          checkbox.checked = result.enabledSources.includes(checkbox.dataset.id);
        });
      }
    });
  }

  // Сохранение состояния
  function saveSettings() {
    const checkboxes = document.querySelectorAll('.source-checkbox input');
    const enabledSources = [];
    
    checkboxes.forEach(checkbox => {
      if (checkbox.checked) {
        enabledSources.push(checkbox.dataset.id);
      }
    });
    
    chrome.storage.sync.set({ enabledSources: enabledSources }, function() {
      statusMessage.classList.add('show');
      setTimeout(() => {
        statusMessage.classList.remove('show');
      }, 2000);
      
      chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, { 
          type: 'SOURCES_UPDATED', 
          sources: enabledSources 
        });
      });
    });
  }

  refreshBtn.addEventListener('click', loadSources);
  saveBtn.addEventListener('click', saveSettings);
  loadSources();
});