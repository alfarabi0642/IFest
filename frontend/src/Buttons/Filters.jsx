import { useState } from "react";

function Filters() {
    return (
        <div className="flex items-center  mr-107 ">
            <button className="transition-all select-none flex justify-center items-center border-solid border-black border-1 
                               rounded-full cursor-pointer font-poppins w-25 h-8 mt-5 text-sm mr-2 hover:shadow-xl hover:bg-secondary
                               hover:border-primary hover:text-white duration-200 bg-white">
                Approved
            </button>
            <button className="transition-all select-none flex justify-center items-center border-solid border-black border-1 
                               rounded-full cursor-pointer font-poppins w-25 h-8 mt-5 text-sm mr-2 hover:shadow-xl hover:bg-secondary 
                               hover:border-primary hover:text-white duration-200 bg-white">
                Indonesia
            </button>
            <button className="transition-all select-none flex justify-center items-center border-solid border-black border-1 
                               rounded-full cursor-pointer font-poppins w-25 h-8 text-sm mr-2 mt-5 hover:shadow-xl hover:bg-secondary 
                               hover:border-primary hover:text-white duration-200 bg-white">
                Monthly
            </button>
            <button className="transition-all select-none flex justify-center items-center border-solid border-black border-1 
                               rounded-full py-1.5 cursor-pointer font-poppins w-30 h-8 text-sm mr-2 mt-5 hover:shadow-xl hover:bg-secondary 
                               hover:border-primary hover:text-white duration-200 bg-white">
                Under Review
            </button>
            <div className="mt-5 ml-58 cursor-pointer transition-all hover:text-primary text-gray-500 font-poppins">Clear Filters</div>
        </div>
    );

}

export default Filters