import axios from "axios";

const token = "ya29.c.b0AXv0zTPWkeiveaWHgJPwLGT3BEc9ldXGIsLCLLeXicebMTnw-MaIG2a499yxp3-Etxu-SzXp-d68Uc82KBcH3MEKiVtsaTWe_-37_vKebrJ-oil7rg9X2A54dZYbq1IjbSGNcyeZ4SsiVNd9uFLTst-GFbTvRYnmoWJ6OyDLcXb3tRS_71X07EIbJM1b6gkr_-iIW3lUuKwe0mTk6VcjfR0rqIO1hRI";
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