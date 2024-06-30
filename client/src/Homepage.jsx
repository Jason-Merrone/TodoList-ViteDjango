import React, { useState, useEffect } from "react";

export default function Homepage(){

  // Function for logging out the user
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