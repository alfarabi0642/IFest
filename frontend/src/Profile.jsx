
function Profile( {username="Guest", role="Admin"} ) {

  return (
    <div className="mt-auto mb-3 flex items-center space-x-3 p-3 bg-white rounded-2xl shadow-md border border-gray-100 max-w-xs mx-auto">
      <div className="relative">
        <img alt="Profile Pic" src="src/assets/profilepic.png" className="rounded-full w-10 h-10"></img>
        <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-white"></div>
      </div>

        <div>
            <h1 className="font-poppinsbold text-sm">{username}</h1>
            <p className="text-xs text-gray-500">{role}</p>
        </div>

    </div>
    );   
}

export default Profile