import ArrowDown from "../assets/arrow_down.svg?react";

function Sort(){
    return(
        <div className="flex justify-betweenborder-solid border-b-gray-500 border-2 
                        rounded py-2 px-5 cursor-pointer font-bold font-poppins"> 
            <h1>Newest</h1>
            <ArrowDown/>
        </div>
    );

}

export default Sort