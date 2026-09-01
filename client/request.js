async function triggerSeriesOfReq(user_id){
  if(user_id > 10){
    console.log("user_id cant exceed 10");
    return;
  }
  const res = await fetch("http://localhost:8000/notify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        user_id: user_id,
        msg: `Hello id ${user_id} Real-time`
      })
    });
    
    const data = await res.json();
    console.log(`req ${user_id} resp : ` , data);
}

for(let i = 1 ; i<=10 ; i++){
  triggerSeriesOfReq(i);
}