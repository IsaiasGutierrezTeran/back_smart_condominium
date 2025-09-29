# Code Citations

## License: unknown
https://github.com/zafarbekde/Data-Mems/tree/df4cf9440916274d85f738d414ab539087ad182b/src/components/LoginForm.jsx

```
} from 'react';
import axios from 'axios';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(
```


## License: unknown
https://github.com/juanez1999/AnastomosisApp/tree/34d9f85f4984cdc2c06e65427c5c2779cf64ad35/src/components/Login/Login.jsx

```
value={email} onChange={e => setEmail(e.target.value)} />
        <input type="password" placeholder="Contraseña" value={password} onChange={e => setPassword(e.target.value)} /
```


## License: unknown
https://github.com/CRYKER7/paperlife-redux/tree/0226bb87449fbad896eae8bce682902e9765d196/src/components/Login.jsx

```
=> setEmail(e.target.value)} />
        <input type="password" placeholder="Contraseña" value={password} onChange={e => setPassword(e.target.value)} />
        <button type="submit">
```


## License: unknown
https://github.com/iMlearnDinG/static-web-app/tree/9866116077126fb80053bc7cfbe6d4dbe2f1e64b/src/config/axiosConfig.js

```
instance = axios.create();

instance.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
```


## License: unknown
https://github.com/kjrocker/custom-fields/tree/00f974ee2ceaa36d590e199ca8ddd9ee1112345b/client/src/api/axios.ts

```
.create();

instance.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

