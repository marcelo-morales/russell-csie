import axios from "axios";

const token = "ya29.c.b0AXv0zTODua7uWNhcGQ5WOAaczOUYFvM52icMfqgQpsxIsDfWtkQfeZY_uPvxnUYUMDAbe4kQ5NHXf4o5TOWH3K-FEEIfpAm7Zn-Y3Yjqrt73S0YaUx9nXb49cJQ4rvx2Dsya188hICYSw1_OgPzxRIvNR6H30FOCToSAJrq9QWftrRZpgo68D6TfOX5OVySj1VImowOvylQ5chUode8VeX0SRNhLEXs";
const axiosInstance = axios.create({
  baseURL: "https://texttospeech.googleapis.com/v1/text:synthesize",
  headers: {
    Authorization: `Bearer ${token}`,
  },
});

async function getAudio(text) {
  const body = {
    input: {
      text: text,
    },
    voice: {
      languageCode: "en-US",
      name: "en-US-Wavenet-A",
      ssmlGender: "MALE",
      // naturalSampleRateHertz: 24000
    },
    audioConfig: {
      audioEncoding: "MP3",
    }
  };
  try {
    const response = await axiosInstance.post('', body);
    return response.data.audioContent;
  } catch (err) {
    throw err;
  }
}

export default getAudio;