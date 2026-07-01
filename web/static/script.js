console.log("SCRIPT LOADED");

const SpeechRecognition =
  window.SpeechRecognition ||
  window.webkitSpeechRecognition;

if (!SpeechRecognition) {

  alert(
    "Speech Recognition not supported in this browser"
  );

} else {

  const recognition =
    new SpeechRecognition();

  let processing = false;

  recognition.lang = "en-IN";
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onstart = () => {

    console.log("Mic Started");

    const status =
      document.getElementById("responseText");

    if (status) {
      status.innerText =
        "Jarvis: Listening...";
    }
  };

  recognition.onresult = async (event) => {

    if (processing) return;

    processing = true;

    const transcript =
      event.results[
        event.results.length - 1
      ][0].transcript;

    console.log(
      "You said:",
      transcript
    );

    const liveText =
      document.getElementById("liveText");

    if (liveText) {
      liveText.innerText =
        "You: " + transcript;
    }

    try {

      const response =
        await fetch("/command", {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            command: transcript,
          }),
        });

      const data =
        await response.json();

      console.log(
        "Server Response:",
        data
      );

      const responseText =
        document.getElementById(
          "responseText"
        );

      if (responseText) {

        if (data.message) {

          responseText.innerText =
            "Jarvis: " +
            data.message;

        } else {

          responseText.innerText =
            "Jarvis: Command Executed";
        }
      }

    } catch (error) {

      console.error(
        "Error:",
        error
      );

      const responseText =
        document.getElementById(
          "responseText"
        );

      if (responseText) {
        responseText.innerText =
          "Jarvis: Error";
      }

    } finally {

      processing = false;
    }
  };

  recognition.onerror = (event) => {

    console.log(
      "Speech Error:",
      event.error
    );

    if (
      event.error === "aborted" ||
      event.error === "no-speech"
    ) {
      return;
    }

    const responseText =
      document.getElementById(
        "responseText"
      );

    if (responseText) {
      responseText.innerText =
        "Jarvis: " +
        event.error;
    }
  };

  recognition.onend = () => {

    console.log("Recognition Ended");
  
    processing = false;
  
    setTimeout(() => {
  
      try {
        console.log("Restarting Mic...");
        recognition.start();
      } catch (e) {
        console.log("Restart Error:", e);
      }
  
    }, 1000);
  };
  try {

    recognition.start();

  } catch (e) {

    console.log(e);
  }
}