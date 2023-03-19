const templates = {
  activityGame: document.getElementById('template-activity-game')
}

const handleSteamActivity = (data) => {
  const steamActivity = templates.activityGame
    .content
    .firstElementChild
    .cloneNode(true)
  
  const gameName = steamActivity.querySelector('#name')
  const gameIcon = steamActivity.querySelector('#icon')
  const gamePlatform = steamActivity.querySelector('#platform')

  gameName.setAttribute('href', data.gameURL)
  gameName.innerHTML = data.gameTitle

  gameIcon.remove()

  gamePlatform.innerHTML = 'Steam'

  document.getElementById('activity').replaceWith(steamActivity)
}

const handleUnknownActivity = (data) => {
  activity.innerHTML = 'Error: Unknown activity'
}

const supportedActivites = {
  'steam': handleSteamActivity,
  'unknown': handleUnknownActivity
}

const requestActivity = () => {
  fetch('/api/activity/')
    .then((response) => response.json())
    .then((data) => {
      if (data.isActive) {
        if (data.platform in supportedActivites) {
          supportedActivites[data.platform](data)
        } else {
          supportedActivites.unknown(data)
        }
      } else {
        document.getElementById('activity').innerHTML = 'No activity.'
      }
    })
}

requestActivity()
