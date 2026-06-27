document.addEventListener('DOMContentLoaded', ()=>{

    // Element Constructor Function
    class SuperElement{
        constructor(type,classes,id){ //classes must be a list
            this.element = document.createElement(type)
            if(Array.isArray(classes)){
                for(const clss of classes){
                    this.element.classList.add(clss)
                }
            }
            if(id){
                this.element.id = id
            }
        }

        detail(lable,value,valueId){
            let lableWrap = document.createElement('div')
            let valueWrap = document.createElement('div')

            let detailLable= document.createElement('strong')
            let detailValue= document.createElement('small')

            lableWrap.classList.add('detail-lable')
            valueWrap.classList.add('detail-value')

            if(valueId){
                detailValue.id = valueId
            }  
            detailLable.textContent = lable
            detailValue.textContent = value

            lableWrap.append(detailLable)
            valueWrap.append(detailValue)

            this.element.append(lableWrap,valueWrap)

        }

        //Create Edit Button 
        createEditButton(dataValue){
            const editButton = document.createElement('button')
            editButton.classList.add('dash-option','edit-button','dialog-action','edit-visit')
            editButton.setAttribute('data-field',dataValue)
            editButton.textContent = 'Edit'
            this.element.append(editButton)

        }
    }

    //Open a list of patients with atleat one visit recorded by current doctor
    allPatientsButton = document.querySelector('#all-patients')
    myPatientsButton = document.querySelector('#my-patients')
    allPatientsNav = document.querySelector('#all-patients-nav')

    dashContainer = document.querySelector('.dash-container')
    dashDataPanel = document.querySelector('.dash-data-panel')
    dashDataGrid = document.querySelector('.dash-data-grid')
    dashOptionsPanel = document.querySelector('.dash-options-panel')


    patientInfoPanel = document.querySelector('#patient-info-panel')
    patientVisitForm = document.querySelector('#new-visit-form')
    patientVisitDetails = document.querySelector('#patient-visit-details')

//view current user's profile
    myProfileButton = document.querySelector('#myProfile')
    myProfileButton.addEventListener('click',(e)=>{
        e.preventDefault()
        fetch('/myProfile')
        .then(response=>{
            if(!response.ok){
                throw new Error("Failed to fetch MY profile")
            }
            return response.json()
        })
        .then(profile=>{
            console.log(profile)

            dashDataPanel.textContent = ''
            dashOptionsPanel.textContent = ''
            profileDetailsContainer = new SuperElement('div',['patient-details-container'],'')
            heading = new SuperElement('h4',['dash-data-heading'],'')
            heading = heading.element
            heading.textContent = `Profile of ${profile[0].doctorName}`

            nameDiv = new SuperElement('div',['details'], '')
            nameDiv.detail('Name :',`${profile[0].user.first_name} ${profile[0].user.last_name}`)
            nameDiv = nameDiv.element

            phoneNumber = new SuperElement('div',['details','patient-detail'],'')
            phoneNumber.detail('Contact :',profile[0].contact)
            phoneNumber = phoneNumber.element
            email = new SuperElement('div',['details','patient-detail'],'')
            email.detail('Email :',profile[0].user.email_address)
            email = email.element
            patientAddress = new SuperElement('div',['details'],'') 
            patientAddress.detail('Address :',profile[0].address)
            patientAddress = patientAddress.element

            specializationDiv = new SuperElement('div',['details'],'' )
            specializationDiv.detail('Specialization :',profile[0].specialization)
            specializationDiv = specializationDiv.element

            detailsContainer1 = new SuperElement('div',['details-container'],'')
            detailsContainer1 = detailsContainer1.element
            detailsContainer1.append(phoneNumber,email)

            profileDetailsContainer.element.append(heading,nameDiv,detailsContainer1,patientAddress,specializationDiv)
            dashDataPanel.append(profileDetailsContainer.element)

            allPatientsButton = new SuperElement('a',['dash-option'],'all-patients')
            allPatientsButton = allPatientsButton.element
            allPatientsButton.textContent = 'All Patients'
                        myPatientsButton = new SuperElement('a',['dash-option'],'my-patients')
            myPatientsButton = myPatientsButton.element
            myPatientsButton.textContent = 'My Patients'
                        newPatientsButton = new SuperElement('a',['dash-option'],'new-patients')
            newPatientsButton = newPatientsButton.element
            newPatientsButton.textContent = 'New Patients'
            newPatientsButton.setAttribute('href',"/patient%20sign%20up")

            dashOptionsPanel.append(allPatientsButton,myPatientsButton,newPatientsButton)

        })
        .catch(error=>{console.log('Error:',error)})
    })

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
            patientName = document.createElement('h4')

            patientCard.element.setAttribute('href',`/view_patient/${patient.user.id}`)

            patientName.textContent = `${patient.user.first_name}`

            patientCard.element.append(patientName)
            newDashDataGrid.element.append(patientCard.element)
        }
        dashDataPanel.append(newDashDataGrid.element)
    }

    //Populate visit fields with visit details
    function populateVisit(data){
            
        visitDetailsContainer = new SuperElement('div',['visit-details-container'],'')
        visitDetailsContainer = visitDetailsContainer.element

        dashDataPanel.textContent = ''
        heading = new SuperElement('h4',['dash-data-heading'],'')
        heading = heading.element
        heading.textContent = ` details of ${data.vitals.visit.visit_date} visit`

        reason = new SuperElement('div',['visit-details'],'')
        reason.detail('Reason For Visit :',data.vitals.visit.reason,'reason')    
        
        vitalsContainer = new SuperElement('div',['vital-details-container'],'')
        vitalsContainer = vitalsContainer.element
        bmiContainer = new SuperElement('div',['vital-details-container'],'')
        bmiContainer = bmiContainer.element

        bp = new SuperElement('div',['details','vital-details'],'')
        bp.detail('BP :', data.vitals.blood_pressure,'bp')
        
        temp = new SuperElement('div',['details','vital-details'],'')
        temp.detail('Temp :', data.vitals.temperature)
        
        pulse = new SuperElement('div',['details','vital-details'],'')
        pulse.detail('Pulse :', data.vitals.heart_rate)
        
        height = new SuperElement('div',['details','vital-details'],'')
        height.detail('hieght :',data.vitals.height)
        
        weight = new SuperElement('div',['details','vital-details'],'')
        weight.detail('weight :',data.vitals.weight)

        diagnosis = new SuperElement('div',['visit-details'],'')
        diagnosis.detail('Diagnosis :',data.vitals.visit.diagnostic)
        
        treatment = new SuperElement('div',['visit-details'],'')
        treatment.detail('Treatment :',data.vitals.visit.treatment)

        notes = new SuperElement('div',['visit-details'],'')
        notes.detail('Notes :',data.vitals.visit.notes)
        
        if(data.user_is_visit_doctor){
            reason.createEditButton('reason')
            bp.createEditButton('bp')
            temp.createEditButton('temp')
            pulse.createEditButton('pulse')
            height.createEditButton('height')
            weight.createEditButton('weight')
            diagnosis.createEditButton('diagnosis')
            treatment.createEditButton('treatment')
            notes.createEditButton('notes')
        }

        reason = reason.element
        bp = bp.element
        temp = temp.element
        pulse = pulse.element
        height = height.element
        weight = weight.element
        diagnosis = diagnosis.element
        treatment = treatment.element
        notes = notes.element

        vitalsContainer.append(bp,temp,pulse)
        bmiContainer.append(height,weight)

        visitDetailsContainer.append(heading,reason,vitalsContainer,bmiContainer,diagnosis,treatment,notes)
        dashDataPanel.append(visitDetailsContainer)
        
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
                heading = new SuperElement('h4',['dash-data-heading'],'')
                heading = heading.element
                heading.textContent = 'Patient Personal Details'

                nameDiv = new SuperElement('div',['details'],'')
                nameDiv.detail('Name',`${info.user.first_name} ${info.user.last_name}`)
                nameDiv = nameDiv.element

                idDiv = new SuperElement('div',['details'],'')
                idDiv.detail('ID',info.patient_id)
                idDiv = idDiv.element

                phoneNumber = new SuperElement('div',['details','patient-detail'],'')
                phoneNumber.detail('Contact',info.contact)
                phoneNumber = phoneNumber.element
                email = new SuperElement('div',['details','patient-detail'],'')
                email.detail('Email',info.user.username)
                email = email.element
                patientAddress = new SuperElement('div',['details','patient-detail'],'') 
                patientAddress.detail('Address',info.address)
                patientAddress = patientAddress.element

                detailsContainer1 = new SuperElement('div',['details-container'],'')
                detailsContainer1 = detailsContainer1.element
                detailsContainer1.append(phoneNumber,email,patientAddress)

                gender = new SuperElement('div',['details','patient-detail'],'')
                gender.detail('Gender :',info.gender)
                gender =gender.element
                bloodType = new SuperElement('div',['details','patient-detail'],'')
                bloodType.detail('Blood Type :', info.blood_type)
                bloodType = bloodType.element

                detailsContainer2 = new SuperElement('div',['details-container'],'')
                detailsContainer2 = detailsContainer2.element
                detailsContainer2.append(gender,bloodType)

                allergies = new SuperElement('div',['details'],'')
                allergies.detail('Allegies :', info.allergies)
                allergies = allergies.element

                patientDetailsContainer.element.append(heading,nameDiv,idDiv,detailsContainer1,detailsContainer2,allergies)
                dashDataPanel.append(patientDetailsContainer.element)

            })
        }

        if(e.target.matches('#patient-visits') || e.target.matches('#cancel-visit-button')){
            e.preventDefault()
            patientId = e.target.dataset.patientId

            fetch(`/visits/${patientId}`)
            .then(response=>{
                if(!response.ok){throw new Error("failed to fetch patient's visits")}
                return response.json()
            })
            .then(visits=>{
                dashDataPanel.textContent = ''
                heading = new SuperElement('h4',['dash-data-heading'],'')
                heading = heading.element
                heading.textContent = 'Patient Visits'

                visitsTable = new SuperElement('table',['visit-details-container','visits-table'], '')
                visitsTable = visitsTable.element

                tableHead = new SuperElement('thead',['table-head'],'')
                tableHead = tableHead.element
                th1 = new SuperElement('th',[],'')
                th2 = new SuperElement('th',[],'')
                th3 = new SuperElement('th',[],'')
                th4 = new SuperElement('th',[],'')
                th1.element.textContent = 'Reason for Visit'
                th2.element.textContent = 'Date'
                th3.element.textContent = 'Doctor'
                th4.element.textContent = 'Action'

                tableHead.append(th1.element,th2.element,th3.element,th4.element)

                tableBody = new SuperElement('tbody',['table-body'],'')
                tableBody =tableBody.element
                for(const visit of visits){
                
                    tableRow = new SuperElement('tr',['details','patient-visit'],'')
                    tableRow = tableRow.element
                    tableRow.setAttribute('data-visit-id',visit.visitId)
                    tableData1 = new SuperElement('td',[])
                    tableData2 = new SuperElement('td',[])
                    tableData3 = new SuperElement('td',[])
                    tableData4 = new SuperElement('td',['action-row'])
                    tableData4 = tableData4.element
                    tableData1.element.textContent = visit.reason
                    tableData2.element.textContent = visit.visit_date
                    tableData3.element.textContent = visit.doctor.doctorName

                    deleteButton = new SuperElement('button',['dash-option','delete-button','dialog-action','delete-visit'])
                    deleteButton = deleteButton.element
                    deleteButton.textContent = 'Delete'
                    deleteButton.setAttribute('data-id',visit.visitId)
                    deleteButton.setAttribute('data-date',visit.visit_date)

                    tableData4.append(deleteButton)

                    tableRow.append(tableData1.element,tableData2.element,tableData3.element,tableData4)
                    tableBody.append(tableRow)
                }
                visitsTable.append(tableHead,tableBody)
                dashDataPanel.append(heading,visitsTable)

            })
        }

        //EventListener for patient visit
        if(e.target.matches('.patient-visit')){
            visitId = e.target.dataset.visitId
            fetch(`/viewVisit/${visitId}`)
            .then(response=>{
                if(!response.ok){throw new Error("Failed to fetch Visit details")}
                return response.json()
            })
            .then(data=>populateVisit(data))
        }

        //EventListerner for Edit visit details button
        if(e.target.matches('.edit-visit')){
            fieldId = e.target.getAttribute('data-field')
            field = document.getElementById(fieldId)
            editTextField = new SuperElement('input',['detail-value-input'],`edit-${fieldId}`)
            editTextField = editTextField.element
            editTextField.type = 'text'
            editTextField.value = field.textContent
            field.parentNode.replaceChild(editTextField, field)
            fieldValue = field.textContent
       
        }
        
        //EventListener for delete User and delete Visit buttons
        if(e.target.matches('#delete-user')||e.target.matches('.delete-visit')){
            alert('deleting')
            e.preventDefault()
            patientName = document.querySelector('.patient-name').textContent
            dialogBox = new SuperElement('div',['message-div'],'')
            dialogBox = dialogBox.element

            messageDiv = new SuperElement('div',['message-container'],'')
            messageDiv = messageDiv.element

            if(e.target.matches('#delete-user')){
                messageDiv.textContent = `Are you sure you want to delete "${patientName}" from the system?`
            }else{
                visitDate = e.target.getAttribute('data-date')
                messageDiv.textContent = `Are you sure you want to delete ${patientName}'s ${visitDate} visit from list ?`

            }

            dialogActionsContainer = new SuperElement('div',['dialog-action-container'],'')
            dialogActionsContainer = dialogActionsContainer.element

            cancelAction = new SuperElement('button',['dash-option','cancel-button','dialog-action'],'cancel-action')
            cancelAction = cancelAction.element
            cancelAction.textContent = 'Cancel' 
            deleteAction = new SuperElement('a',['dash-option','confirm-button','dialog-action'],'delete-action')
            deleteAction = deleteAction.element

            if(e.target.matches('#delete-user')){
                deleteAction.addEventListener('click', ()=>{
                    deleteUrl = document.querySelector('.delete-button').getAttribute('data-url')
                    deleteAction.setAttribute('href', deleteUrl)
                })

            }else{
                deleteAction.addEventListener('click', ()=>{

                    visitId =e.target.getAttribute('data-id')

                    fetch(`/remove_visit/${visitId}`)
                    .then(response=>{
                        if(!response.ok){throw new Error("failed to fetch patient's visits")}

                        visitDiv = document.querySelector('[data-visit-id="1"]')
                        visitDiv.remove()
                        dialogBox.remove()
                        return
                    })
                })
            }
            
            deleteAction.textContent = 'Delete'

            dialogActionsContainer.append(cancelAction,deleteAction)

            dialogBox.append(messageDiv,dialogActionsContainer)
            dashContainer.append(dialogBox)

            cancelAction.addEventListener('click',()=>{
                dialogBox.remove()
            })
        }
    })

})
