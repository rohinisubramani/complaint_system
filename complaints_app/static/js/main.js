/**
 * Complaint Management System JavaScript Frontend Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  // Auto-dismiss alert notifications after 5 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.5s ease';
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });

  // Client-Side Registration Form Validation
  const registerForm = document.getElementById('registerForm');
  if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
      const password = document.getElementById('password').value;
      const confirmPassword = document.getElementById('confirm_password').value;
      
      if (password !== confirmPassword) {
        e.preventDefault();
        alert('Passwords do not match. Please re-enter passwords.');
        return false;
      }
      
      if (password.length < 6) {
        e.preventDefault();
        alert('Password must be at least 6 characters long.');
        return false;
      }
    });
  }

  // Client-Side Submit Complaint Validation
  const complaintForm = document.getElementById('complaintForm');
  if (complaintForm) {
    complaintForm.addEventListener('submit', (e) => {
      const title = document.getElementById('title').value.trim();
      const category = document.getElementById('category').value;
      const description = document.getElementById('description').value.trim();
      const location = document.getElementById('location').value.trim();

      if (!title || !category || !description || !location) {
        e.preventDefault();
        alert('Please fill out all required fields.');
        return false;
      }
    });
  }
});

// Admin Status Modal Toggle Functions
function openAdminModal(complaintId, currentStatus, currentResponse) {
  const modal = document.getElementById('updateModal');
  if (modal) {
    document.getElementById('modalComplaintId').textContent = complaintId;
    document.getElementById('updateForm').action = `/admin-complaints/${complaintId}/update/`;
    
    const statusSelect = document.getElementById('modalStatusSelect');
    if (statusSelect) {
      statusSelect.value = currentStatus;
    }
    
    const responseTextarea = document.getElementById('modalAdminResponse');
    if (responseTextarea) {
      responseTextarea.value = currentResponse || '';
    }
    
    modal.classList.add('active');
  }
}

function closeAdminModal() {
  const modal = document.getElementById('updateModal');
  if (modal) {
    modal.classList.remove('active');
  }
}

// Client-Side Live Filter Table Search (Instant Table Filter)
function filterTableBySearch(inputId, tableId) {
  const input = document.getElementById(inputId);
  const filter = input.value.toLowerCase();
  const table = document.getElementById(tableId);
  if (!table) return;
  
  const trs = table.getElementsByTagName('tr');
  for (let i = 1; i < trs.length; i++) {
    const tdText = trs[i].textContent.toLowerCase();
    if (tdText.indexOf(filter) > -1) {
      trs[i].style.display = '';
    } else {
      trs[i].style.display = 'none';
    }
  }
}
