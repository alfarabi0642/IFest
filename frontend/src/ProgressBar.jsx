
function ProgressBar() {
    return (
        <div className="flex my-7 items-center justify-center hover:scale-103 transition-all duration-76">
            <div className="w-[15rem] rounded-full bg-gray-500">
                <div className="bg-primary h-full rounded-full w-[70%] text-white font-poppins
                                font-medium p-0.5 text-xs text-center ">70%
                </div>
            </div>
        </div>
    );
}

export default ProgressBar;