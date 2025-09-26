import Plus from "../assets/Plus.svg?react";

function Add(){
    return(
        <div className="bg-white hover:shadow-md select-none flex justify-center items-center border-solid border-black border-1
                        rounded-full py-1.5 px-4 cursor-pointer font-poppins w-22 mt-5 mr-106"> 
            <Plus/>
            Add
        </div>
    );
}

export default Add