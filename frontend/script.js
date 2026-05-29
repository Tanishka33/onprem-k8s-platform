const backendURL = "/api";

async function loadFeedbacks() {

    const response = await fetch(`${backendURL}/feedback`);
    const data = await response.json();

    const feedbackList = document.getElementById("feedbackList");

    feedbackList.innerHTML = "";

    data.forEach(item => {

        feedbackList.innerHTML += `
            <div style="border:1px solid black; padding:10px; margin:10px;">
                <p><b>Name:</b> ${item.name}</p>
                <p><b>Date:</b> ${item.date}</p>
                <p><b>Feedback:</b> ${item.feedback}</p>

                <button onclick="deleteFeedback(${item.id})">
                    Delete
                </button>
            </div>
        `;
    });
}

async function submitFeedback() {

    const name = document.getElementById("name").value;
    const date = document.getElementById("date").value;
    const feedback = document.getElementById("feedback").value;

    await fetch(`${backendURL}/feedback`, {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            name,
            date,
            feedback
        })
    });

    loadFeedbacks();
}

async function deleteFeedback(id) {

    await fetch(`${backendURL}/feedback/${id}`, {
        method: "DELETE"
    });

    loadFeedbacks();
}

loadFeedbacks();