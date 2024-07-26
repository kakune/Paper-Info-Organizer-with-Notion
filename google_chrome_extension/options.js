function saveOptions() {
    const Notion_API_Key = document.getElementById('Notion_API_Key').value;
    const Database_ID = document.getElementById('Database_ID').value;
    const Keywords_ID = document.getElementById('Keywords_ID').value;
    chrome.storage.sync.set({ Notion_API_Key: Notion_API_Key, Database_ID: Database_ID, Keywords_ID: Keywords_ID }, () => {
      alert('IDs saved.');
    });
  }
  
  function restoreOptions() {
    chrome.storage.sync.get(['Notion_API_Key', 'Database_ID', 'Keywords_ID'], (data) => {
      document.getElementById('Notion_API_Key').value = data.Notion_API_Key || '';
      document.getElementById('Database_ID').value = data.Database_ID || '';
      document.getElementById('Keywords_ID').value = data.Keywords_ID || '';
    });
  }
  
  document.getElementById('save').addEventListener('click', saveOptions);
  document.addEventListener('DOMContentLoaded', restoreOptions);
  