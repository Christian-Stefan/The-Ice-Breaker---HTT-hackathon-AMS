import fetch from "node-fetch";

async function callGreenPT() {
    const response = await fetch("https://api.greenpt.ai/v1/chat/completions", {
      method: "POST",
      headers: {"Content-Type": "application/json", "Authorization": "Bearer sk-CpkdZT1zSlekZOrSv8htAdFeYeiAPkIlqlBuvoyX-vQ",},
      body: JSON.stringify({model: "green-l", messages: [{role: "user", content: "What is the top story on hotnewhiphop.com right now?"}], stream: false}),
    });
  
    const data: any = await response.json();
    console.log(data["choices"][0]['message']['content']);
  }
  
async function getTools() {
  const response = await fetch("https://api.greenpt.ai/v1/chat/completions", {
    method: "POST",
    headers: {"Content-Type": "application/json", "Authorization": "Bearer sk-CpkdZT1zSlekZOrSv8htAdFeYeiAPkIlqlBuvoyX-vQ",},
    body: JSON.stringify({model: "green-l", messages: [{role: "user", content: "What is the top story on hotnewhiphop.com right now?"}], stream: false}),
  });
}

callGreenPT();
