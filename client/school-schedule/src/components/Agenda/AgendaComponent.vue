<template>
  <div id="app">
    <div class="table-container">
      <!-- Tabela para dispositivos maiores -->
      <table border="1" v-if="!isMobile">
        <thead>
          <tr>
            <th v-for="coluna in colunas" :key="coluna">{{ coluna }}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td v-for="coluna in colunas" :key="coluna">
              <div class="cards-container">
                <div
                  class="card"
                  v-for="i in 10"
                  :key="`${coluna}-${i}`"
                  @click="abrirModalDisciplina(coluna, i)"
                >
                  <template v-if="aulaExiste(coluna, i)">
                    <div>
                      <h4>{{ aulaPorPosicao(coluna, i).disciplina }}</h4>
                      <img
                        v-if="aulaPorPosicao(coluna, i).professor_foto"
                        :src="getProfessorFotoUrl(aulaPorPosicao(coluna, i).professor_foto)"
                        alt="Foto do Professor"
                        class="foto-professor"
                      />
                      <p>Horário: {{ aulaPorPosicao(coluna, i).horario }}</p>
                    </div>
                  </template>
                  <template v-else>
                    <p>Sem aula</p>
                  </template>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Exibição no celular como slide -->
      <div v-else class="mobile-slide">
        <h3>{{ colunas[colunaAtiva] }}</h3>
        <div class="cards-container">
          <div
            class="card"
            v-for="i in 10"
            :key="`${colunas[colunaAtiva]}-${i}`"
            @click="abrirModalDisciplina(colunas[colunaAtiva], i)"
          >
            <template v-if="aulaExiste(colunas[colunaAtiva], i)">
              <div>
                <h4>{{ aulaPorPosicao(colunas[colunaAtiva], i).disciplina }}</h4>
                <img
                  v-if="aulaPorPosicao(colunas[colunaAtiva], i).professor_foto"
                  :src="getProfessorFotoUrl(aulaPorPosicao(colunas[colunaAtiva], i).professor_foto)"
                  alt="Foto do Professor"
                  class="foto-professor"
                />
                <p>Horário: {{ aulaPorPosicao(colunas[colunaAtiva], i).horario }}</p>
              </div>
            </template>
            <template v-else>
              <p>Sem aula</p>
            </template>
          </div>
        </div>
        <div class="navigation-buttons">
          <button @click="mudarDia(-1)" :disabled="colunaAtiva === 0">&#8592; Anterior</button>
          <button @click="mudarDia(1)" :disabled="colunaAtiva === colunas.length - 1">Próximo &#8594;</button>
        </div>
      </div>
    </div>

    <!-- ModalDisciplina -->
    <modal-disciplina
      v-if="modalDisciplinaVisivel"
      :dia="diaSelecionado"
      :card="cardSelecionado"
      @fechar="fecharModalDisciplina"
      @salvar="salvarDisciplina"
    />
  </div>
</template>

<script>
import api from "../../api.js";
import ModalDisciplina from "./ModalDisciplina.vue";

export default {
  components: {
    ModalDisciplina,
  },
  data() {
    return {
      colunas: ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"],
      colunaAtiva: 0,
      isMobile: window.innerWidth <= 768,
      modalDisciplinaVisivel: false,
      diaSelecionado: "",
      cardSelecionado: null,
      aulas: [],
    };
  },
  mounted() {
    this.atualizarDiaAtivo();
    window.addEventListener("resize", this.handleResize);
    this.carregarAgenda();
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.handleResize);
  },
  methods: {
    handleResize() {
      this.isMobile = window.innerWidth <= 768;
    },
    atualizarDiaAtivo() {
      const hoje = new Date();
      const diaSemana = hoje.getDay();
      this.colunaAtiva = diaSemana === 0 ? 5 : diaSemana - 1;
    },
    mudarDia(direcao) {
      const novoDia = this.colunaAtiva + direcao;
      if (novoDia < 0 || novoDia >= this.colunas.length) return;
      this.colunaAtiva = novoDia;
    },
    getProfessorFotoUrl(foto) {
      return foto.startsWith("/media/")
        ? `http://127.0.0.1:8000${foto}`
        : foto;
    },
    aulaExiste(dia, card) {
      return this.aulas.some((aula) => aula.dia === dia && aula.card === card);
    },
    aulaPorPosicao(dia, card) {
      return this.aulas.find((aula) => aula.dia === dia && aula.card === card);
    },
    abrirModalDisciplina(dia, card) {
      this.diaSelecionado = dia;
      this.cardSelecionado = card;
      this.modalDisciplinaVisivel = true;
    },
    fecharModalDisciplina() {
      this.modalDisciplinaVisivel = false;
    },
    async salvarDisciplina(dados) {
      try {
        await api.post("/agendas/", dados);
        this.carregarAgenda();
        this.fecharModalDisciplina();
      } catch (error) {
        console.error("Erro ao salvar disciplina:", error);
      }
    },
    async carregarAgenda() {
      try {
        const response = await api.get("/agendas/");
        this.aulas = response.data.map((agenda) => ({
          id: agenda.id,
          dia: agenda.dia,
          card: agenda.card || 1,
          horario: agenda.horario,
          disciplina: agenda.disciplina_nome || "Disciplina não encontrada",
          professor_foto: agenda.professor_foto || "",
        }));
      } catch (error) {
        console.error("Erro ao carregar a agenda:", error);
      }
    },
  },
};
</script>

<style scoped>
.table-container {
  margin: 20px;
}

.cards-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card {
  padding: 15px;
  text-align: center;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 5px;
  cursor: pointer;
}

.card:hover {
  background: #e9ecef;
}

.foto-professor {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin: 10px 0;
  object-fit: cover;
}

.mobile-slide .cards-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

.navigation-buttons button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.navigation-buttons button:hover {
  background-color: #0056b3;
}
</style>
