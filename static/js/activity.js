let activity = document.getElementById('activity')
const templates = {
  activityGame: document.getElementById('template-activity-game')
}

const handleGameActivity = (data) => {
  const gameActivity = templates.activityGame
    .content
    .firstElementChild
    .cloneNode(true)
  
  const gameName = gameActivity.querySelector('#name')
  const gameIcon = gameActivity.querySelector('#icon')
  const gamePlatform = gameActivity.querySelector('#platform')

  gameName.setAttribute('href', data.gameURL)
  gameName.innerHTML = data.gameTitle

  gameIcon.setAttribute('style', `background-image: url("${data.gameIconURL}")`)
  if (data.platform === 'steam') {
    gameIcon.remove()
  }

  gamePlatform.innerHTML = data.platform === 'steam' ? 'Steam' : 'VK Play'
  if (data.platform === 'steam' && data.isVKPCloud) {
    gamePlatform.innerHTML = 'Steam using a VK Play Cloud'
  }

  activity.replaceWith(gameActivity)
  activity = gameActivity

  let darkestColor = 'rgb(0, 0, 0)'
  fetch(data.gameWallpaper.apiURL)
    .then((response) => {
      console.log(response.headers)
      darkestColor = response.headers.get('x-darkest-color')

      return response.blob()
    })
    .then((blob) => {
      const backgroundURL = URL.createObjectURL(blob)
      document.body.setAttribute('style', `
        background-color: ${darkestColor};
        background-image: url("${backgroundURL}");
        background-repeat: no-repeat;
        background-size: 100vw;
      `)
    })
}

const handleUnknownActivity = (data) => {
  activity.innerHTML = 'Error: Unknown activity'
}

const supportedActivites = {
  'steam': handleGameActivity,
  'vkp': handleGameActivity,
  'unknown': handleUnknownActivity
}

const requestActivity = () => {
  document.body.removeAttribute('style')

  activity.classList.add('loading')
  activity.innerHTML = 'Updating the activity information...'

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

setInterval(requestActivity, 60 * 30 * 1000)
requestActivity()
