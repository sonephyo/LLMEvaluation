import axios from "axios";
import { BACKEND_URL } from "../../config/config";
import { LLMResponseData } from "../../interface/interface";
import { useEffect, useState } from "react";
import Markdown from "react-markdown";

interface PopUpDataInterface {
  isOpen: boolean;
  response: string;
}

export const PromptStorage = () => {
  const [allLLMData, setallLLMData] = useState<LLMResponseData[] | null>(null);
  const [popUpDataInterface, setpopUpDataInterface] =
    useState<PopUpDataInterface>({
      isOpen: false,
      response: "",
    });

  useEffect(() => {
    axios.get(`${BACKEND_URL}/data`).then((res) => setallLLMData(res.data));
    return () => {
      setallLLMData(null);
    };
  }, []);

  return (
    <div className="">
      {allLLMData && (
        <table className="table-auto border-collapse border border-gray-300 w-full">
          <thead className="bg-gray-100">
            <tr>
              <th className="border border-gray-300 px-4 py-2">AI Model</th>
              <th className="border border-gray-300 px-4 py-2">
                System Prompt
              </th>
              <th className="border border-gray-300 px-4 py-2">
                Content Prompt
              </th>
              <th className="border border-gray-300 px-4 py-2">Response</th>

              <th className="border border-gray-300 px-4 py-2">Score</th>
            </tr>
          </thead>
          <tbody>
            {allLLMData.map((result, index) => (
              <tr
                className={` dark:bg-gray-800 dark:text-white`}
                key={index}
              >
                <td className="border border-gray-300 px-4 py-2">
                  {result.aiModel}
                </td>
                <td className="border border-gray-300 px-4 py-2">
                  {result.systemPrompt}
                </td>
                <td className="border border-gray-300 px-4 py-2">
                  {result.contentPrompt}
                </td>
                <td className="border border-gray-300 px-4 py-2">
                  <button
                    className="bg-blue-500 text-white px-4 py-1 rounded hover:bg-blue-600"
                    onClick={() => {
                      setpopUpDataInterface({
                        isOpen: true,
                        response: result.response,
                      });
                    }}
                  >
                    View Response
                  </button>
                </td>

                <td className="border border-gray-300 px-4 py-2">
                  {result.score}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <PopUpViewResponse
        isOpen={popUpDataInterface.isOpen}
        response={popUpDataInterface.response}
        setPopUpDataInterface={setpopUpDataInterface}
      />
    </div>
  );
};
const PopUpViewResponse = (props: {
  isOpen: boolean;
  response: string;
  setPopUpDataInterface: React.Dispatch<
    React.SetStateAction<PopUpDataInterface>
  >;
}) => {
  return (
    <div
      id="info-popup"
      tabIndex={1}
      className={`${
        props.isOpen ? "block" : "hidden"
      } fixed inset-0 z-50 flex items-center justify-center`}
    >
      <div className="relative p-4 w-11/12 md:w-1/2 h-full md:h-auto">
        <div className="relative p-4 bg-white rounded-lg shadow dark:bg-gray-800 md:p-8">
          <div className="mb-4 text-sm font-light text-gray-500 dark:text-gray-400">
            <span
              className="bg-slate-700 rounded-full flex items-center justify-center text-3xl font-bold uppercase absolute -right-4 -top-4 w-10 h-10 text-white hover:bg-blue-200 hover:duration-200 cursor-pointer"
              onClick={() => {
                props.setPopUpDataInterface((prev) => ({
                  ...prev,
                  isOpen: false,
                }));
              }}
            >
              <img src="/cross-white.svg" alt="X" />
            </span>
            <Markdown>{props.response}</Markdown>
          </div>
        </div>
      </div>
    </div>
  );
};
