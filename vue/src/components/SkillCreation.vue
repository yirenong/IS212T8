<template>
    <div class="container mb-2 mt-2">
        <h4>Create New Skill</h4>
        <hr>
        
        <form @submit.prevent="createSkill">
            <div class="form-group">
                <label for="skillName">Skill Name:</label><br><br>
                <input type="text" id="skillName" v-model="skillName" class="form-control"/>
            </div>
            <br>
            <button type="submit" class="btn btn-success mb-2">Create Skill</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            skillName: '',
            skillList: []
        };
    },
    created() {
        this.getAllSkill();

    },
    methods: {
        getAllSkill(){
            axios.get('http://localhost:5000/api/skill_list')
            .then(response => {
                this.skillList = response.data.map(item => item.Skill_Name);
                console.log('Skill List:', this.skillList);
            })
            .catch(error => {
                console.error('Error fetching skill list:', error);
            });
        },
        checkSkill(){
            if (this.skillList.includes(this.skillName)){
                return true;
            }
            else{
                return false;
            }

        },
        createSkill() {
            const data = {
                Skill_Name: this.skillName
            };
            if (this.checkSkill() === true){
                alert('Skill already exists');
            }
            else if (this.skillName === ""){
                alert('Skill name cannot be empty');
            }
            else{
                axios.post('http://localhost:5000/api/skill', data)
                    .then(response => {
                        if (response.status === 201) {
                            console.log('Skill created successfully');
                            alert('Skill created successfully');
                            this.skillName = ''; 
                        } else {
                            console.error('Failed to create skill');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            }
        },
    },
};
</script>
