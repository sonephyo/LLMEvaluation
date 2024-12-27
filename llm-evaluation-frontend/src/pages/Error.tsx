import { SideBar } from "../App";

export const Error = () => {
  return (
    <div className="">
      <SideBar />
      <div>
        <div className="p-4 sm:ml-64">
          <div className="p-4 border-2 border-gray-200 border-dashed rounded-lg dark:border-gray-700">
            <h1>Page Not Found</h1>
          </div>
        </div>
      </div>
    </div>
  );
};
