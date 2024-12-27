import axios from "axios";
import { useState } from "react";
import { BACKEND_URL } from "../../config/config";

interface PromptInterface {
  systemPrompt: string;
  contentPrompt: string;
}

export const GeneratePrompt = () => {
  const [formData, setFormData] = useState({
    systemPrompt: "",
    contentPrompt: "",
  });

  const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    const { id, value } = event.target;
    setFormData((prevData: PromptInterface) => ({
      ...prevData,
      [id]: value,
    }));
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    console.log("Form Data:", formData);

    for (const value of Object.values(formData)) {
      if (!value) {
        alert("One of the input is empty");
        return;
      }
    }

    axios
      .post(`${BACKEND_URL}/ai`, formData)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  };
  return (
    <div className="flex justify-center">
      <form onSubmit={handleSubmit} className="mb-5 w-1/2">
        <div className="my-10">
          <label
            htmlFor="systemPrompt"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            System Prompt - Input what you want the LLM to know
          </label>
          <textarea
            id="systemPrompt"
            value={formData.systemPrompt}
            onChange={handleChange}
            className="block w-full p-4 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 text-base focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>
        <div className="my-10">
          <label
            htmlFor="contentPrompt"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Content Prompt
          </label>
          <textarea
            id="contentPrompt"
            value={formData.contentPrompt}
            onChange={handleChange}
            className="block w-full p-4 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 text-base focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>
        <button
          type="submit"
          className="w-full mx-auto text-white bg-gradient-to-br from-purple-600 to-blue-500 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2"
        >
          Generate Response
        </button>
      </form>

      <ResultResponse />
    </div>
  );
};

const ResultResponse = () => {
  return 
};
