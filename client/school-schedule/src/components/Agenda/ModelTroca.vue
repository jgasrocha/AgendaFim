<template>
    <div class="modal-overlay">
      <div class="modal">
        <h3>Solicitar Troca de Aula</h3>
  
        <!-- Campo: Sua Aula -->
        <p><strong>Sua Aula:</strong></p>
        <select v-model="suaAula" class="form-select">
          <option disabled value="">Selecione sua aula</option>
          <option v-for="aula in suasAulas" :key="aula.id" :value="aula">
            {{ aula.dia }} - {{ aula.horario }}
          </option>
        </select>
  
        <!-- Campo: Aula do Outro Professor -->
        <p><strong>Aula do Outro Professor:</strong></p>
        <div class="aula-input">
          <label for="diaOutro">Dia:</label>
          <select v-model="aulaNovaDia" id="diaOutro" class="form-select">
            <option disabled value="">Selecione o dia</option>
            <option v-for="dia in diasSemana" :key="dia" :value="dia">
              {{ dia }}
            </option>
          </select>
  
          <label for="horarioOutro">Horário:</label>
          <select v-model="aulaNovaHorario" id="horarioOutro" class="form-select">
            <option disabled value="">Selecione o horário</option>
            <option v-for="horario in horariosDisponiveis" :key="horario" :value="horario">
              {{ horario }}
            </option>
          </select>
        </div>
  
        <div v-if="aulaNova" class="aula-selecionada">
          <p><strong>Aula Selecionada:</strong></p>
          <p>{{ aulaNova.disciplina }} - {{ aulaNova.professor }}</p>
        </div>
  
        <!-- Botões -->
        <div class="modal-buttons">
          <button @click="salvar" :disabled="!suaAula || !aulaNova">Enviar Troca</button>
          <button @click="$emit('fechar')">Cancelar</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      aulas: Array, // Todas as aulas disponíveis
      suasAulas: Array, // Apenas as aulas do professor autenticado
    },
    data() {
      return {
        suaAula: null, // Aula selecionada do professor autenticado
        aulaNovaDia: '', // Dia selecionado no campo "Aula do Outro Professor"
        aulaNovaHorario: '', // Horário selecionado no campo "Aula do Outro Professor"
      };
    },
    computed: {
      diasSemana() {
        return ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
      },
      horariosDisponiveis() {
        const horarios = this.aulas
          .filter(aula => aula.dia === this.aulaNovaDia)
          .map(aula => aula.horario);
        return [...new Set(horarios)]; // Remove duplicatas
      },
      aulaNova() {
        if (!this.aulaNovaDia || !this.aulaNovaHorario) return null;
        return this.aulas.find(
          aula => aula.dia === this.aulaNovaDia && aula.horario === this.aulaNovaHorario
        );
      },
    },
    methods: {
      salvar() {
        if (this.suaAula && this.aulaNova) {
          const troca = {
            suaAula: this.suaAula.id,
            novaAula: this.aulaNova.id,
          };
          this.$emit("salvar", troca);
        }
      },
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
  
  .aula-input {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 15px;
  }
  
  .form-select {
    width: 100%;
    padding: 5px;
    border-radius: 4px;
    border: 1px solid #ccc;
  }
  
  .aula-selecionada {
    margin: 15px 0;
    padding: 10px;
    background-color: #f9f9f9;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .modal-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
  }
  
  button {
    padding: 10px 20px;
    font-size: 14px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  
  button:not(:disabled) {
    background-color: #007bff;
    color: white;
  }
  </style>
  