import Form from "../Form.jsx";

function Login() {
    return(
        <div className="w-full h-screen flex border-1 items-center justify-center bg-gray-100">
            <div className="w-full h-full lg:w-1/2 flex flex-col items-center justify-center">
                <Form/>
                <p className="bootm-0 mt-3 font-poppins">&copy; ILCSense, 2025 - Bljr</p>
            </div>
            {/*<div className="bg-gray-200 hidden relative h-full lg:w-1/2 lg:flex items-center justify-center">
                <div className="w-60 h-60 bg-gradient-to-tr from-primary to-secondary rounded-full animate-bounce"></div>
                <div className="w-full h-full bottom-0 bg-white/10 backdrop-blur-lg absolute animate-pulse"></div>
            </div> */}
        </div>
    );
}

export default Login;