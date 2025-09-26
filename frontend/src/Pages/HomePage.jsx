
import Button from "../Button.jsx"

function HomePage( {username} ){
    username = 'Ishaq Irfan F'
    return (
        <div className="mt-5 ml-53 p-6">
            <h1 className="text-3xl font-poppinsbold mt-2">Welcome Back, {username}!</h1>
            <Button />
        </div>
    );
}
export default HomePage