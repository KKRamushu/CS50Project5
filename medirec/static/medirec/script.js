document.addEventListener('DOMContentLoaded', ()=>{

    // Element Constructor Function
    function SuperElement(type,classes,id){ //classes must be a list
        this.element = document.createElement(type)
        for(const clss of classes){
            this.element.classList.add(clss)
        }
        if(id != ''){
            this.element.setAttribute('id',id)
        }
        return this.element
    }

    //Open a list of patients with atleat one visit recorded by current doctor
    allPatientsButton = document.querySelector('#all-patients')
    myPatientsButton = document.querySelector('#my-patients')
    allPatientsNav = document.querySelector('#all-patients-nav')

    dashContainer = document.querySelector('.dash-container')
    dashDataPanel = document.querySelector('.dash-data-panel')
    dashDataGrid = document.querySelector('.dash-data-grid')

    patientInfoPanel = document.querySelector('#patient-info-panel')
    patientVisitForm = document.querySelector('#new-visit-form')
    patientVisitDetails = document.querySelector('#patient-visit-details')

    //event listener for patients viewing buttons
    function allPatientsListener(dashDataPanel){
  
        fetch('/allPatients/')
        .then(response=>{
            if(!response.ok){
                throw new Error("Failed to fetch all patients from server")
            }
            return response.json()
        })
        .then(patients=>{
            load_patients(patients,dashDataPanel) 
        })
        .catch(error=>{console.log('Error:',error)})
    } 

    // populate dashboard with patients
    function load_patients(patients,dashDataPanel){
        dashDataPanel.textContent = ''
        const newDashDataGrid = new SuperElement('div',['dash-data-grid'],'')
        for(const patient of patients){
            const patientCard = new SuperElement('a',['patient-card'],'')
            const patientName = document.createElement('h4')

            patientCard.setAttribute('href',`/view_patient/${patient.user.id}`)

            patientName.textContent = `${patient.user.first_name}`

            patientCard.append(patientName)
            newDashDataGrid.append(patientCard)
        }
        dashDataPanel.append(newDashDataGrid)
    }

    dashContainer.addEventListener('click',function(e){
        // add an event listener if the "all patients button exists"
        if(e.target.matches("#all-patients")){
            e.preventDefault()//prevents "a" element default behavior
            allPatientsListener(dashDataPanel)
        }

        // add an event listener if the "my patients button exists"
        if(e.target.matches("#my-patients")){
            e.preventDefault() //prevents "a" element default behavior
            fetch('/myPatients/')
            .then(response=> {
                if(!response.ok){
                    throw new Error("Failed to fetch my patients")  
                }
                return response.json()})
            .then(patients =>{
                load_patients(patients,dashDataPanel)
                
            })
            .catch(error=>{console.error('Error:',error)})
        }

        //add patient info listener
        if(e.target.matches("#patient-info")){
            e.preventDefault()
            patientId = e.target.dataset.patientId
            dashDataPanel.textContent = ''

            fetch(`/patient_info/${patientId}`)
            .then(response=>{
                if(!response.ok){throw new Error("failed to fetch patient info")}
                return response.json()
            })
            .then(info=>{
                patientDetailsContainer = new SuperElement('div',['patient-details-container'],'')
                heading = new SuperElement('h4',[],'')
                heading.textContent = 'Personal details'

                nameDiv = new SuperElement('div',['details'],'')
                nameLable = new SuperElement('strong',['detail-lable'],'')
                nameLable.textContent = 'Name:'
                patientName = new SuperElement('small',['detail-value'],'')
                patientName.textContent = `${info.user.first_name} ${info.user.last_name}`
                nameDiv.append(nameLable,patientName)

                idDiv = new SuperElement('div',['details'],'')
                idLable = new SuperElement('strong',['detail-lable'],'')
                idLable.textContent = 'ID:'
                patientId = new SuperElement('small',['detail-value'],'')
                patientId.textContent = info.patient_id
                idDiv.append(idLable,patientId)

                detailsContainer1 = new SuperElement('div',['details-container'],'')

                contactDiv = new SuperElement('div',['details','patient-detail'],'')
                contactLabel = new SuperElement('strong',['detail-lable'],'')
                contactLabel.textContent = 'Contact'
                contactValue = new SuperElement('small',['detail-value'],'')
                contactValue.textContent = info.contact
                contactDiv.append(contactLabel, contactValue)

                emailDiv = new SuperElement('div',['details','patient-detail'],'')
                emailLabel = new SuperElement('strong',['detail-lable'],'')
                emailLabel.textContent = 'Email'
                emailValue = new SuperElement('small',['detail-value'],'')
                emailValue.textContent = info.user.email
                emailDiv.append(emailLabel, emailValue)

                addressDiv = new SuperElement('div',['details','patient-detail'],'')
                addressLabel = new SuperElement('strong',['detail-lable'],'')
                addressLabel.textContent = 'Address'
                addressValue = new SuperElement('small',['detail-value'],'')
                addressValue.textContent = info.address
                addressDiv.append(addressLabel, addressValue)

                detailsContainer1.append(contactDiv, emailDiv, addressDiv)

                detailsContainer2 = new SuperElement('div',['details-container'],'')
                genderDiv = new SuperElement('div',['details','patient-detail'],'')
                genderLabel = new SuperElement('strong',['detail-lable'],'')
                genderLabel.textContent = 'Gender'
                genderValue = new SuperElement('small',['detail-value'],'')
                genderValue.textContent = info.gender
                genderDiv.append(genderLabel, genderValue)

                bloodDiv = new SuperElement('div',['details','patient-detail'],'')
                bloodLabel = new SuperElement('strong',['detail-lable'],'')
                bloodLabel.textContent = 'Blood Type'
                bloodValue = new SuperElement('small',['detail-value'],'')
                bloodValue.textContent = info.blood_type
                bloodDiv.append(bloodLabel, bloodValue)

                detailsContainer2.append(genderDiv, bloodDiv)

                allergyDiv = new SuperElement('div',['details'],'')

                allergyLabel = new SuperElement('strong',['detail-lable'],'')
                allergyLabel.textContent = 'Allergies'
                allergyValue = new SuperElement('small',['detail-value'],'')
                allergyValue.textContent = info.allergies
                editBtn = new SuperElement('input',[],'')
                editBtn.type = 'button'
                editBtn.value = '✏️'
                allergyDiv.append(allergyLabel, allergyValue, editBtn)


                patientDetailsContainer.append(heading,nameDiv,idDiv,detailsContainer1,detailsContainer2,allergyDiv)
                dashDataPanel.append(patientDetailsContainer)

            })
        }

        if(e.target.matches('#patient-visits')){
            e.preventDefault()
            patientId = e.target.dataset.patientId

            fetch(`/visits/${patientId}`)
            .then(response=>{
                if(!response.ok){throw new Error("failed to fetch patient's visits")}
                return response.json()
            })
            .then(visits=>{
                dashDataPanel.textContent = ''
                heading = new SuperElement('h4',[],'')
                heading.textContent = 'Patient Visits'

                visitsTable = new SuperElement('table',['visit-details-container','visits-table'], '')

                tableHead = new SuperElement('thead',['table-head'],'')
                th1 = new SuperElement('th',[],'')
                th2 = new SuperElement('th',[],'')
                th3 = new SuperElement('th',[],'')
                th1.textContent = 'Reason for Visit'
                th2.textContent = 'Date'
                th3.textContent = 'Doctor'
                tableHead.append(th1,th2,th3)

                tableBody = new SuperElement('tbody',['table-body'],'')
                for(const visit of visits){
                
                    tableRow = new SuperElement('tr',['details','patient-visit'],'')
                    tableRow.setAttribute('data-visit-id',visit.visitId)
                    tableData1 = new SuperElement('td',[])
                    tableData2 = new SuperElement('td',[])
                    tableData3 = new SuperElement('td',[])
                    tableData1.textContent = visit.reason
                    tableData2.textContent = visit.visit_date
                    tableData3.textContent = visit.doctor.doctorName

                    tableRow.append(tableData1,tableData2,tableData3)
                    tableBody.append(tableRow)
                }
                visitsTable.append(tableHead,tableBody)
                dashDataPanel.append(heading,visitsTable)

            })
        }

        if(e.target.matches('.patient-visit')){
            visitId = e.target.dataset.visitId
            fetch(`/viewVisit/${visitId}`)
            .then(response=>{
                if(!response.ok){throw new Error("Failed to fetch Visit details")}
                return response.json()
            })
            .then(visit=>{
                console.log(visit)
            })
        }
    })

})
