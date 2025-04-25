import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import UserLogin from './Components/User/Authentication';
import UserRegistration from './Components/User/Registration';


function App() {

  const [page, setPage] = useState("login")

  
  return(

    <>
      <h1>Blog Application</h1>
      {page === "login" && <UserLogin/>}
      {page === "registration" && <UserRegistration/>}
      {page === "login" && <button onClick={() => setPage("registration")}>{page}</button>}
      {page === "registration" && <button onClick={() => setPage("login")}>{page}</button>}
      
    </>
    
   

  )
}




export default App;
