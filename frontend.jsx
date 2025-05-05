import React, { useState } from "react";

export default function LatexPaperCompilerUI() {
  const [latexCode, setLatexCode] = useState("");
  const [textContent, setTextContent] = useState("");
  const [pdfUrl, setPdfUrl] = useState("");

  const handleLatexChange = (e) => {
    const value = e.target.value;
    // Optional: Add validation to allow only LaTeX syntax if needed
    setLatexCode(value);
  };

  const handleCompile = () => {
    // Placeholder: Replace this with actual compilation and PDF URL fetch logic
    // For example, sending a request to a backend service that compiles the LaTeX code
    setPdfUrl("/path/to/generated/output.pdf");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 to-white p-6">
      <h1 className="text-3xl font-bold text-center mb-6 text-gray-800">
        Research Paper Compiler
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Output Section */}
        <div className="md:col-span-1 border-2 border-black rounded-2xl p-4 shadow-xl bg-white">
          <h2 className="text-xl font-bold mb-2 text-gray-700">Output</h2>
          <div className="h-[500px] overflow-auto border border-gray-300 rounded-lg p-4 bg-gray-50 flex items-center justify-center">
            {pdfUrl ? (
              <iframe
                src={pdfUrl}
                className="w-full h-full"
                title="Compiled PDF Output"
              ></iframe>
            ) : (
              <span className="text-gray-400">Compiled PDF will appear here</span>
            )}
          </div>
        </div>

        <div className="md:col-span-1 space-y-6">
          {/* LaTeX Code Input */}
          <div className="border-2 border-black rounded-2xl p-4 shadow-xl bg-white">
            <h2 className="text-xl font-bold mb-2 text-gray-700">LaTeX Code</h2>
            <textarea
              className="w-full h-60 border border-gray-300 rounded-lg p-2 font-mono text-sm bg-gray-50"
              placeholder="Enter LaTeX template here..."
              value={latexCode}
              onChange={handleLatexChange}
            ></textarea>
          </div>

          {/* Text Input */}
          <div className="border-2 border-black rounded-2xl p-4 shadow-xl bg-white">
            <h2 className="text-xl font-bold mb-2 text-gray-700">
              Text Input (Contents of the Paper)
            </h2>
            <textarea
              className="w-full h-60 border border-gray-300 rounded-lg p-2 text-sm bg-gray-50"
              placeholder="Enter research paper content here..."
              value={textContent}
              onChange={(e) => setTextContent(e.target.value)}
            ></textarea>
          </div>

          <div className="text-center">
            <button
              onClick={handleCompile}
              className="bg-blue-600 text-white px-6 py-2 rounded-xl shadow hover:bg-blue-700 transition"
            >
              Compile to PDF
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
