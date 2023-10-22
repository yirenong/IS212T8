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
        };
    },
    methods: {
        createSkill() {
            const data = {
                Skill_Name: this.skillName
            };

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
        },
    },
};
</script>
