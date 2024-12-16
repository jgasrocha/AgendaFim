<template>
  <div class="modal-overlay">
    <div class="modal">
      <h3>Escolher Disciplina</h3>

      <select v-model="selectedDisciplina" @change="atualizarProfessorFoto">
        <option v-for="disciplina in disciplinas" :key="disciplina.id" :value="disciplina.id">
          {{ disciplina.nome }}
        </option>
      </select>

      <div class="professor-info" v-if="professorFoto">
        <!-- Verifique se a URL é válida e completa -->
        <img :src="professorFoto.startsWith('/media/') ? 'http://127.0.0.1:8000' + professorFoto : professorFoto"
          alt="Foto do Professor" />
        <p>Professor: {{ professorNome }}</p>
      </div>

      <div class="modal-buttons">
        <button @click="salvar">Salvar Aula</button>
        <button @click="$emit('fechar')">Cancelar</button>
      </div>
    </div>
  </div>
</template>


<script>
import api from '../../api';

export default {
  props: {
    dia: String,
    card: Number,
  },
  data() {
    return {
      disciplinas: [],
      selectedDisciplina: null,
      professorFoto: null,
      professorNome: '',
    };
  },
  async mounted() {
    try {
      const response = await api.get('/disciplinas/');
      this.disciplinas = response.data;
    } catch (error) {
      console.error('Erro ao carregar disciplinas:', error);
    }
  },
  methods: {
    atualizarProfessorFoto() {
      const disciplina = this.disciplinas.find(d => d.id === this.selectedDisciplina);
      if (disciplina && disciplina.professor_foto) {
        this.professorFoto = disciplina.professor_foto;  // Foto retornada pela API
        this.professorNome = disciplina.professor_nome;
      } else {
        this.professorFoto = null;
        this.professorNome = '';
      }
    },
    salvar() {
      if (this.selectedDisciplina) {
        const dados = {
          dia: this.dia,
          disciplina: this.selectedDisciplina,
        };
        this.$emit("salvar", dados); // Emite os dados para o componente pai
      } else {
        alert("Por favor, selecione uma disciplina.");
      }
    }

  },
};
</script>


<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
}

.professor-info {
  margin: 20px 0;
  text-align: center;
}

.professor-info img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
}
</style>
