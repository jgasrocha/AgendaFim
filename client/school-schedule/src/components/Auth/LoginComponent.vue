<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin">
      <h2>Login</h2>

      <div class="form-group">
        <label for="email">Email:</label>
        <input
          type="email"
          id="email"
          v-model="email"
          placeholder="Digite seu email"
          required
        />
      </div>

      <div class="form-group">
        <label for="password">Senha:</label>
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="Digite sua senha"
          required
        />
      </div>

      <button type="submit">Entrar</button>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/login/", {
          email: this.email,
          password: this.password,
        });

        // Redireciona para a página de agenda em caso de sucesso
        this.$router.push("/agenda");
      } catch (error) {
        console.error("Erro ao fazer login:", error.response?.data || error.message);
        this.errorMessage =
          error.response?.data?.error || "Erro ao fazer login. Verifique suas credenciais.";
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

form {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 300px;
}

h2 {
  margin-bottom: 20px;
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.error {
  margin-top: 10px;
  color: red;
  text-align: center;
}
</style>
