import ProfilePic from "../assets/profilepic.png"
import Button from "../Button.jsx"

function HomePage( {username} ){
    username = 'Ishaq Irfan F'
    return (
        <div className="mt-5 ml-53 p-6 h-screen">
            <h1 className="text-3xl font-poppinsbold mt-2">Welcome Back, {username}!</h1>
            <div className="relative w-full items-center justify-center ">
                <img src={ProfilePic} className="mt-30 w-100 h-100 mx-auto rounded-full animate-bounce"/>
            </div>
            <div className="w-full h-1/2  bg-white/10 backdrop-blur-lg absolute "></div>
        </div>
    );
}
export default HomePage