const socket = io();
const emailList = document.getElementById("email-list");
const refreshBtn = document.getElementById("refresh");
const protocolRadios = document.getElementsByName("protocol");

// دالة لجلب الإيميلات حسب البروتوكول المختار
function fetchEmails() {
  let selectedProtocol = "IMAP";
  protocolRadios.forEach(radio => {
    if (radio.checked) selectedProtocol = radio.value;
  });

  if (selectedProtocol === "IMAP") {
    socket.emit("fetch_imap_emails");
  } else {
    socket.emit("fetch_pop3_emails");
  }
}

// بعد الاتصال بالـ SocketIO، طلب الرسائل مباشرة
socket.on("connect", () => {
  console.log("Connected to SocketIO server");
  fetchEmails();
});

// زر لتحديث الإيميلات يدويًا
refreshBtn.addEventListener("click", fetchEmails);

// عرض الإيميلات عند استقبال الحدث
socket.on("emails_data", data => {
  const { emails, error } = data;
  emailList.innerHTML = "";

  if (error) {
    const li = document.createElement("li");
    li.textContent = `⚠️ Error: ${error}`;
    emailList.appendChild(li);
    return;
  }

  if (!emails || emails.length === 0) {
    const li = document.createElement("li");
    li.textContent = "No emails found.";
    emailList.appendChild(li);
    return;
  }

  emails.forEach(email => {
    const li = document.createElement("li");

    const fromEl = document.createElement("p");
    fromEl.innerHTML = `<strong>From:</strong> ${email.from}`;

    const subjectEl = document.createElement("p");
    subjectEl.innerHTML = `<strong>Subject:</strong> ${email.subject}`;

    const bodyEl = document.createElement("p");
    bodyEl.innerHTML = `<strong>Body:</strong> ${email.body}`;

    li.appendChild(fromEl);
    li.appendChild(subjectEl);
    li.appendChild(bodyEl);

    emailList.appendChild(li);
  });
});
