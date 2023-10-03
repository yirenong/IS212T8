<template>
    <div>
        <h2>Search Candidates</h2>
        <!-- select to filter  -->
        <select v-model="selectedSkill" @change="onChange($event)">
            <option value="All">All</option>
            <option v-for="(skill, index) in skill_list" :key="index" :value="skill.Skill_ID">
                {{ skill.Skill_Name }}
            </option>
        </select>
        
        
        <table>
            <thead>
                <tr>
                    <th>Staff ID</th>
                    <th>Staff Name</th>
                    <th> Department</th>
                    <th>Staff Skills</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(staff, index) in filtered_staff_skill" :key="index">
                    <td>{{ staff.Staff_ID }}</td>
                    <td>{{ staff.Staff_FName + staff.Staff_LName }}</td>
                    <td>{{ staff.Dept }}</td>
                    <td>
                        <ul>
                            <li v-for="(skill, skillIndex) in staff.Skills" :key="skillIndex">
                                {{ skill_list[parseInt(skill)-1].Skill_Name }}
                            </li>
                        </ul>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
  
<script>
import axios from 'axios';

export default {
    data() {
        return {
            selectedSkill: 'All',
            skill_list: [],
            staff_skill: [],
            filtered_staff_skill: []
        };
    },
    methods: {
        onChange(){
            console.log(this.selectedSkill);
            if (this.selectedSkill == 'All') {
                this.filtered_staff_skill = this.staff_skill;
            } else {
                this.filtered_staff_skill = this.staff_skill.filter(staff => staff.Skills.includes(this.selectedSkill));
                
            }
        }
    },
    created() {
        axios.get('http://localhost:5000/api/skill_list')
            .then(response => {
                this.skill_list = response.data;
                console.log('Job Listings:', this.skill_list);
            })
            .catch(error => {
                console.error('Error fetching job listings:', error);
            });
        axios.get('http://localhost:5000/api/staff_skill')
            .then(response => {
                this.staff_skill = response.data;
                this.filtered_staff_skill = this.staff_skill;
                console.log('staff_skill Listings:', this.staff_skill);
            })
            .catch(error => {
                console.error('Error fetching candidate listings:', error);
            });


    },
};
</script>
  
  
  