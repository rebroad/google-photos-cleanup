import React from "/node_modules/.vite/deps/react.js?v=2a84352f";
import ReactDOM from "/node_modules/.vite/deps/react-dom_client.js?v=2a84352f";

window.$RefreshReg$ = window.$RefreshReg$ || (() => {});
window.$RefreshSig$ = window.$RefreshSig$ || (() => (type) => type);

const { default: Playground } = await import("/src/components/playground/Playground.tsx");
ReactDOM.createRoot(document.getElementById("root")).render(React.createElement(Playground));
