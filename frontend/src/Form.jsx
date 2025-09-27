

function Form(){
    return(
        <div className="bg-white rounded-4xl px-12 py-17 items-center justify-center font-poppins h-auto shadow-sm">
            <h1 className="text-center text-5xl mb-9 text-primary font-poppinsbold text-shadow-lg text-shadow-gray-400/75">ILC<a className="text-black">Sense</a></h1>
            <h1 className="text-5xl font-poppins mt-5 flex justify-center font-semibold ">Welcome Back!</h1>
            <p className="text-xl text-gray-500 mt-3">Welcome back, please log in.</p>
            <div>
                <div className="mt-10">
                    <label className="text-lg">E-mail</label>
                    <br></br>
                    <input className="border-1 w-full border-gray-400 rounded-xl p-2 mt-1" placeholder="Enter your e-mail"/>
                    
                </div>
                <div className="mt-5">
                    <label className="text-lg">Password</label>
                    <br/>
                    <input className="border-1 w-full border-gray-400 rounded-xl p-2 mt-1" placeholder="Enter your password"
                    type="password"
                    />
                </div>
                <div className="flex justify-between">
                    <div className="mt-5 select-none">
                        <input 
                            type="checkbox"
                            id="remember"
                        />
                        <label htmlFor="remember" className="ml-1 text-md">Remember me</label>
                    </div>
                    <button className="text-primary cursor-pointer mt-5 hover:text-indigo-700 text-md hover:scale-102">
                        Forgot Password?
                    </button>
                </div>
                <div className="flex flex-col justify-center mt-6">
                    <button className="bg-primary rounded-xl p-3 text-white font-medium 
                                    cursor-pointer active:scale-[.98] active:duration-75 transition-all
                                    hover:scale-102">
                        Sign in
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Form