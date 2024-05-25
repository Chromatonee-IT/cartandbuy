new Card({
  form: 'form',
  container: '.cc-card',
  formSelectors: {
    numberInput: 'input[name=number]',
    expiryInput: 'input[name=expiry]',
    cvcInput: 'input[name=cvv]',
    nameInput: 'input[name=name]'
  },

  width: 390, // optional — default 350px
  formatting: true,

  placeholders: {
    number: '•••• •••• •••• ••••',
    name: 'Full Name',
    expiry: '••/••',
    cvc: '•••'
  }
})