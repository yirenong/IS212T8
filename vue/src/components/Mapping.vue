<template>
    <div>
        <h1>Role to Skill Mapping</h1>
        <table>
            <thead>
                <tr>
                    <th>Role ID</th>
                    <th>Skill ID</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(skill, index) in skills" :key="index">
                    <td>{{ skill.role_id }}</td>
                    <td>{{ skill.skill_id }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    data() {
        return {
            skills: [
                { role_id: 1, skill_id: 101 },
                { role_id: 1, skill_id: 102 },
                { role_id: 2, skill_id: 103 },
                { role_id: 2, skill_id: 104 },
                { role_id: 3, skill_id: 105 },
                { role_id: 3, skill_id: 106 },
            ],
        };
    },
};
</script>
