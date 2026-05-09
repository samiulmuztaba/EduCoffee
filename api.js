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
        batch_codes: user.batch_codes,
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

async function CreateNewBatch(batch) {
  try {
    const response = await fetch(`${api_url}/new_batch`, {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        name: batch.name,
        year: batch.year,
        schedule: batch.schedule,
        teacher_id: batch.teacher_id,
        code: batch.code,
      }),
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

console.log(GetBatchesByTID('a94d1725-95cd-475e-94f5-d03756dda886'))

async function GetMyNotices(teacher_id) {
  try {
    const response = await fetch(`${api_url}/my_notices/${teacher_id}`, {
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

async function CreateNotice(notice) {
  console.log(notice.text)
  try {
    const response = await fetch(`${api_url}/new_notice`, {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        text: notice.text,
        teacher_id: notice.teacher_id,
        batch_codes: notice.batch_codes,
      })
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

async function GetNoticesForStudent(student_id) {
  try {
    const response = await fetch(`${api_url}/notices/${student_id}`, {
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