

export default function Homepage(){
  async function logout() {
      const res = await fetch("/registration/logout/", {
        credentials: "same-origin", // include cookies!
      });
    
      if (res.ok) {
        // navigate away from the single page app!
        window.location = "/registration/sign_in/";
      } else {
        console.log("Yo wtf why this not working?")
      }
    }
  return (
    <>
      <button onClick={logout}>Logout</button>
    </>
  )
}