chrome.action.onClicked.addListener((tab) => {
    let url = tab.url;
    console.log("Current Tab URL: ", url);
  
    chrome.storage.sync.get(['Notion_API_Key', 'Database_ID', 'Keywords_ID'], (data) => {
      let Notion_API_Key = data.Notion_API_Key;
      let Database_ID = data.Database_ID;
      let Keywords_ID = data.Keywords_ID || '';
      console.log("IDs: ", Notion_API_Key, Database_ID, Keywords_ID);
  
      if (!url || !Notion_API_Key || !Database_ID) {
        console.error('Error: One or more required values are missing');
        return;
      }
  
      fetch('http://localhost:5000/run_script', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({url: url, ids: [Notion_API_Key, Database_ID, Keywords_ID]})
      }).then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.text();
      }).then(data => {
        console.log("Server response: ", data);
      }).catch(error => {
        console.error('Fetch error:', error);
      });
    });
  });
  