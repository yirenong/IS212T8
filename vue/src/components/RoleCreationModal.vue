<template>
  <div class="mx-auto">
    <button
      type="button"
      class="btn btn-warning text-white"
      data-bs-toggle="modal"
      data-bs-target="#myModal"
    >
      Create Role
    </button>
    <!-- Modal -->
    <div
      class="modal fade mt-5"
      tabindex="-1"
      id="myModal"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-body">
            <div class="container">
              <!-- 1st Row Primary Details -->
              <div class="row my-3 p-3" style="background-color: #edf1f9">
                <div class="col mx-auto">
                  <h3>Primary Details</h3>
                  <div class="row">
                    <div class="col-4">
                      <div class="form-group">
                        <label for="title">Title:</label>
                        <input
                          type="text"
                          class="form-control"
                          id="title"
                          v-model="modalData.title"
                        />
                      </div>
                    </div>
                    <div class="col-4">
                      <h6>Age:</h6>
                      <p class="fw-normal fs-5">test</p>
                    </div>
                    <div class="col-4">
                      <h6>Gender:</h6>
                      <p class="fw-normal fs-5">test</p>
                    </div>
                  </div>

                  <div class="row">
                    <div class="col-4">
                      <div class="form-group">
                        <label for="title">Title:</label>
                        <input
                          type="text"
                          class="form-control"
                          id="title"
                          v-model="modalData.title"
                        />
                      </div>
                    </div>
                    <div class="col-4">
                      <h6>Age:</h6>
                      <p class="fw-normal fs-5">test</p>
                    </div>
                    <div class="col-4">
                      <h6>Gender:</h6>
                      <p class="fw-normal fs-5">test</p>
                    </div>
                  </div>
                </div>
              </div>

              <div class="row my-3 p-3" style="background-color: #edf1f9">
                <div class="col">
                  <h3>Consultation Record</h3>
                  <h6 class="mt-1 mb-2 text-decoration-underline">
                    Medication Prescribed:
                  </h6>
                  <div class="row mt-4">
                    <h6 class="mt-1 mb-2 text-decoration-underline">
                      Diagnosis:
                    </h6>
                  </div>
                </div>
              </div>

              <div class="row my-3 p-3">
                <div class="col">
                  <button
                    type="button"
                    class="btn btn-outline-danger"
                    data-bs-dismiss="modal"
                  >
                    Close
                  </button>
                </div>
                <div class="col text-end">
                  <button
                    @click="saveConsultation"
                    type="button"
                    class="btn btn-primary"
                    data-bs-dismiss="modal"
                  >
                    Save Consultation
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      modalData: {
        title: "",
      },
    };
  },
  methods: {
    changeMessage() {
      this.message = "New Message";
    },
  },
};
</script>

<style scoped>
/* Your component-specific CSS goes here */
</style>
