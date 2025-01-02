import axios from "axios";
import { useEffect, useState } from "react";
import { BACKEND_URL } from "../../config/config";
import {
  LLMResponse,
  PromptInterface,
  ResultResponesInterface,
} from "../../interface/interface";
import Markdown from "react-markdown";

interface PopUpExistingInterface {
  isOpen: boolean;
  selectedSystemPrompt: string | null;
}

export const GeneratePrompt = () => {
  const [formData, setFormData] = useState<PromptInterface>({
    systemPrompt: "",
    contentPrompt: "",
  });
  const [response, setresponse] = useState<LLMResponse[] | null>(null);
  const [popUpExistingPrompt, setpopUpExistingPrompt] =
    useState<PopUpExistingInterface>({
      isOpen: false,
      selectedSystemPrompt: null,
    });

  useEffect(() => {
    if (popUpExistingPrompt.selectedSystemPrompt != null) {
      setFormData({
        systemPrompt: popUpExistingPrompt.selectedSystemPrompt,
        contentPrompt: "",
      });
    }
  }, [popUpExistingPrompt.selectedSystemPrompt]);

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
      .post(`${BACKEND_URL}/ai/`, formData)
      .then((response) => {
        console.log(response.data);
        setresponse(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <div className="flex justify-center flex-col items-center ">
      <form onSubmit={handleSubmit} className="mb-5 w-1/2">
        <div className="my-10">
          <div className="mb-2 text-sm flex flex-row gap-3">
            <label
              htmlFor="systemPrompt"
              className="block font-medium text-gray-900 dark:text-white"
            >
              System Prompt - Input what you want the LLM to know
            </label>
            <div className="dark:text-white">
              <p
                className="underline cursor-pointer"
                onClick={() => {
                  console.log("clicked");
                  setpopUpExistingPrompt((prev) => ({ ...prev, isOpen: true }));
                }}
              >
                Existing Responses
              </p>
            </div>
          </div>
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
            Content Prompt - Test Cases against the System Prompt
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
      {response && <ResultResponse data={response} />}
      {popUpExistingPrompt.isOpen && (
        <PopUpExistingPrompts setPopUpExistingPrompt={setpopUpExistingPrompt} />
      )}
    </div>
  );
};

const ResultResponse: React.FC<ResultResponesInterface> = (props) => {
  return (
    <div>
      <h1 className="dark:text-white text-4xl m-10">Responses</h1>
      <div className="dark:text-white flex flex-row flex-wrap justify-center gap-2">
        {props.data.map((result, index) => (
          <div
            className="w-[calc(50%-0.5rem)] p-5 flex flex-col items-center"
            key={index}
          >
            <h1 className=" text-3xl mb-3">{result.aiModel}</h1>
            <Markdown>{result.response}</Markdown>
          </div>
        ))}
      </div>
    </div>
  );
};

interface systemPromptInterface {
  id: number;
  systemPrompt: string;
}

const PopUpExistingPrompts = (props: {
  setPopUpExistingPrompt: React.Dispatch<
    React.SetStateAction<PopUpExistingInterface>
  >;
}) => {
  const [systemPrompts, setsystemPrompts] = useState<
    systemPromptInterface[] | null
  >(null);

  useEffect(() => {
    axios.get(`${BACKEND_URL}/ai/systemPrompts`).then((res) => {
      setsystemPrompts(res.data);
    });

    return () => {
      setsystemPrompts(null);
    };
  }, []);

  return (
    <div
      id="info-popup"
      tabIndex={1}
      className={`absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 shadow-md rounded-lg`}
    >
      <div className="relative p-4 w-full h-full md:h-auto">
        <div className="relative p-4 bg-white rounded-lg shadow dark:bg-gray-800 md:p-8">
          <div className="mb-4 text-sm font-light text-gray-500 dark:text-gray-400">
            <span
              className="bg-slate-700 rounded-full flex items-center justify-center text-3xl font-bold uppercase absolute -right-4 -top-4 w-10 h-10 text-white hover:bg-blue-200 hover:duration-200 cursor-pointer"
              onClick={() => {
                props.setPopUpExistingPrompt((prev) => ({
                  ...prev,
                  isOpen: false,
                }));
              }}
            >
              <img src="/cross-white.svg" alt="X" />
            </span>
            <table className="table-auto border-collapse border border-gray-300 w-full">
              <thead className="bg-slate-700">
                <tr>
                  <th className="px-4 py-2">System Prompt</th>
                  <th className="px-4 py-2"></th>
                </tr>
              </thead>
              <tbody>
                {systemPrompts &&
                  systemPrompts.map((item, index) => (
                    <tr
                      className={`dark:bg-gray-800 dark:text-white`}
                      key={index}
                    >
                      <td className=" px-4 line-clamp-2">
                        {item.systemPrompt}
                      </td>
                      <td className="px-4 py-2">
                        <button
                          onClick={() => {
                            props.setPopUpExistingPrompt({
                              isOpen: false,
                              selectedSystemPrompt: item.systemPrompt,
                            });
                          }}
                        >
                          Select
                        </button>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
