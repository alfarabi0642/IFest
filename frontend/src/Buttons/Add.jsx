import Plus from "../assets/Plus.svg?react";
import { useState } from "react";

function Add(){
    return(
        <div
            className="bg-white hover:shadow-md select-none text-sm flex justify-center items-center border-solid border-black border-1
                        rounded-full cursor-pointer font-poppins w-22 mt-2 mr-106 h-8"> 
            <Plus/>
            Add
        </div>
    );
}

export default Add