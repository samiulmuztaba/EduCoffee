const api_url = "http://127.0.0.1:8000/api";

async function Register(user, role) {
  try {
    const response = await fetch(`${api_url}/register`, {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        name: user.name,
        email: user.email,
        password: user.password,
        phone: user.phone,
        center_name: user.center_name,
        role: role,
        batch_code: user.batch_code,
      }),
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail);
    }

    const data = await response.json();
    console.log(data);
    return data;
  } catch (error) {
    console.log(error.message);
  }
}

async function GetUserByID(id) {
  try {
    const response = await fetch(`${api_url}/user/${id}`, {
      method: "GET",
      headers: {
        "Content-type": "application/json",
      },
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail);
    }

    const data = await response.json();
    console.log(data);
    return data;
  } catch (error) {
    console.log(error.message);
    window.location.href = "index.html";
    alert(error.message);
  }
}

async function Login(email, pass) {
  try {
    const response = await fetch(`${api_url}/login`, {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        email: email,
        password: pass,
      }),
    });
    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail);
    }
    const data = await response.json();
    console.log(data);
    return data;
  } catch {
    err;
  }
  {
    console.log(err.message);
  }
}

async function GetBatchesByTID(teacher_id) {
  try {
    const response = await fetch(`${api_url}/batches/${teacher_id}`, {
      method: "GET",
      headers: {
        "Content-type": "application/json",
      },
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail);
    }
    const data = await response.json();
    console.log(data);
    return data;
  } catch (err) {
    console.log(err.message);
  }
}


GetBatchesByTID('3e71c941-110c-4300-be24-ec7f50513a1d')