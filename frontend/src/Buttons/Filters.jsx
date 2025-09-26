import { useState } from "react";

function Filters() {
    return (
        <div className="flex">
            <button className="transition-all select-none flex justify-center items-center border-solid border-black border-1 
                               rounded-full py-1.5 px- cursor-pointer font-poppins w-30 mt-5 text mr-3.5 hover:shadow-xl hover:bg-secondary
                               hover:border-primary hover:text-white duration-200 bg-white">
                Approved
            </button>
            <button className="transition-all select-none flex justify-center items-center border-solid border-black border-1 
                               rounded-full py-1.5 px-4 cursor-pointer font-poppins w-30 mt-5 text mr-3.5 hover:shadow-xl hover:bg-secondary 
                               hover:border-primary hover:text-white duration-200 bg-white">
                Indonesia
            </button>
            <button className="transition-all select-none flex justify-center items-center border-solid border-black border-1 
                               rounded-full py-1.5 px-4 cursor-pointer font-poppins w-25 mt-5 text mr-3.5 hover:shadow-xl hover:bg-secondary 
                               hover:border-primary hover:text-white duration-200 bg-white">
                Monthly
            </button>
            <button className="transition-all select-none flex justify-center items-center border-solid border-black border-1 
                               rounded-full py-1.5 px-4 cursor-pointer font-poppins w-38 mt-5 text mr-3.5 hover:shadow-xl hover:bg-secondary 
                               hover:border-primary hover:text-white duration-200 bg-white">
                Under Review
            </button>
            <div className="mt-6.5 ml-7 cursor-pointer transition-all hover:text-primary text-gray-500 font-poppins">Clear Filters</div>
        </div>
    );

}

export default Filters