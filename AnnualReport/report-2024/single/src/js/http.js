// http.js
import axios from 'axios';

const instance = axios.create({
  baseURL: '', // 设置基础路径
  timeout: 100000, // 设置超时时间
  headers: {
    'Content-Type': 'application/json', // 设置请求头
    // 'Content-Type': 'application/x-www-form-urlencoded',
  }
});

export default instance;
