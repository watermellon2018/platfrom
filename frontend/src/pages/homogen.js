import { useEffect, useRef } from "react";


const HomogenPage = () => {




    return (
        <iframe
            src="http://localhost:3000/App.tsx"
            seamless
            style={{
                height: '100%',
                border: 'none',
                overflow: 'hidden',
                display: 'block',
                width: '100%'
            }}
            // id="my-iframe"
            // onLoad={() => {
            //     const iframe = document.getElementById("my-iframe");
            //     const iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
            //     const height = iframeDocument.body.scrollHeight;
            //     iframe.style.height = `${height}px`;
            // }}
        />

    );
};

export default HomogenPage;
