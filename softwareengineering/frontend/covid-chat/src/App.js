import logo from './logo.svg';
import './App.css';
import React from 'react';

import Chat, { Bubble, useMessages } from "@chatui/core";
import "@chatui/core/dist/index.css";

const initialMessages = [
  {
    type: 'text',
    content: { text: 'Good day! I am your Covid-19 FAQ buddy, how may I help you?' },
    user: { avatar: '//gw.alicdn.com/tfs/TB1DYHLwMHqK1RjSZFEXXcGMXXa-56-62.svg' },
  },
  {
    type: 'image',
    content: {
      picUrl: '//img.alicdn.com/tfs/TB1p_nirYr1gK0jSZR0XXbP8XXa-300-300.png',
    },
  },
];

export default function App() {
  const { messages, appendMsg, setTyping } = useMessages(initialMessages);

  // function getClassification(question) {
  //   // const response = await fetch(`/t/${question}`, {
  //   //   method: 'GET'
  //   // });
  //   return fetch(`/t/${question}`)
  //     .then(response => response.json())
  //     .then(data => {
    
  //       console.warn('-----result', data);
  //       return data;
  //     });
  // }

  function handleSend(type, val) {
    if (type === "text" && val.trim()) {
      appendMsg({
        type: "text",
        content: { text: val },
        position: "right"
      });

      setTyping(true);

      setTimeout(async () => {

        // fetch(``)


        const response = await fetch(`http://localhost:8000/t/${val}`);
        const responseJson = await response.json();
        console.warn('-----responseJson', responseJson);

        // const result = JSON.parse(JSON.stringify(responseJson));

        const responseText = `${responseJson['category']}`;
            appendMsg({
              type: "text",
              content: { text: responseText }
            });

      }, 1000);
    }
  }

  function renderMessageContent(msg) {
    const { content } = msg;
    return <Bubble content={content.text} />;
  }

  return (
    <Chat locale="en-US" 
      navbar={{ title: "Covid FAQ Assistant" }}
      messages={messages}
      renderMessageContent={renderMessageContent}
      onSend={handleSend}
      placeholder={"please type here..."}
    />
  );
}
// what is your routine for the covid holidays