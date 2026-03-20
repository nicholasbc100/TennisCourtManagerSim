"use strict";

(function () {
  var gameLengthDays = 30;
  var state = {};

  var statsNode = document.getElementById("stats");
  var logNode = document.getElementById("log");
  var runDayButton = document.getElementById("runDayButton");
  var maintenanceButton = document.getElementById("maintenanceButton");
  var marketingButton = document.getElementById("marketingButton");
  var buildButton = document.getElementById("buildButton");
  var tournamentButton = document.getElementById("tournamentButton");
  var restartButton = document.getElementById("restartButton");

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function createInitialState() {
    return {
      day: 1,
      money: 1500,
      members: 70,
      courts: 3,
      reputation: 50,
      courtCondition: 72,
      happiness: 60,
      gameOver: false
    };
  }

  function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  function log(message) {
    var line = document.createElement("div");
    line.textContent = "[Day " + state.day + "] " + message;
    logNode.prepend(line);
  }

  function formatMoney(value) {
    var sign = value < 0 ? "-$" : "$";
    return sign + Math.abs(value);
  }

  function updateStats() {
    var statusText = state.gameOver
      ? "Finished"
      : state.day > gameLengthDays
      ? "Victory"
      : "In Progress";
    statsNode.innerHTML =
      '<div class="stat"><span class="label">Day</span><span class="value">' +
      state.day +
      "/" +
      gameLengthDays +
      '</span></div><div class="stat"><span class="label">Money</span><span class="value">' +
      formatMoney(state.money) +
      '</span></div><div class="stat"><span class="label">Members</span><span class="value">' +
      state.members +
      '</span></div><div class="stat"><span class="label">Courts</span><span class="value">' +
      state.courts +
      '</span></div><div class="stat"><span class="label">Reputation</span><span class="value">' +
      state.reputation +
      '</span></div><div class="stat"><span class="label">Court Condition</span><span class="value">' +
      state.courtCondition +
      '%</span></div><div class="stat"><span class="label">Happiness</span><span class="value">' +
      state.happiness +
      '%</span></div><div class="stat"><span class="label">Status</span><span class="value">' +
      statusText +
      "</span></div>";

    var disabled = state.gameOver || state.day > gameLengthDays;
    runDayButton.disabled = disabled;
    maintenanceButton.disabled = disabled;
    marketingButton.disabled = disabled;
    buildButton.disabled = disabled;
    tournamentButton.disabled = disabled;
  }

  function spend(cost, actionName) {
    if (state.gameOver || state.day > gameLengthDays) {
      return false;
    }
    if (state.money < cost) {
      log("Not enough money for " + actionName + ".");
      return false;
    }
    state.money -= cost;
    return true;
  }

  function runDay() {
    if (state.gameOver || state.day > gameLengthDays) {
      return;
    }

    var weatherPenalty = randomInt(0, 18);
    var demand = state.reputation + state.happiness - weatherPenalty;
    var maxBookings = state.courts * 18;
    var bookings = clamp(Math.floor(demand / 3), 10, maxBookings);
    var revenue = bookings * 7;
    var operatingCost = 95 + state.courts * 18 + (100 - state.courtCondition);
    var net = revenue - operatingCost;
    state.money += net;

    var memberChange =
      Math.floor((state.happiness + state.reputation - 105) / 20) +
      randomInt(-1, 1);
    state.members = clamp(state.members + memberChange, 25, 350);

    state.courtCondition = clamp(
      state.courtCondition - randomInt(3, 7) - Math.floor(bookings / 20),
      0,
      100
    );
    state.happiness = clamp(
      state.happiness +
        (state.courtCondition > 55 ? 1 : -2) +
        (bookings < maxBookings / 2 ? 1 : -1),
      0,
      100
    );
    state.reputation = clamp(
      state.reputation + (memberChange > 0 ? 1 : memberChange < 0 ? -1 : 0),
      0,
      100
    );

    log(
      "Bookings: " +
        bookings +
        ", net: " +
        formatMoney(net) +
        ", members change: " +
        (memberChange >= 0 ? "+" : "") +
        memberChange
    );

    if (state.money < -400 || state.happiness < 20 || state.courtCondition < 15) {
      state.gameOver = true;
      log("Club collapsed. Try a better strategy!");
    } else if (state.day >= gameLengthDays) {
      state.day = gameLengthDays + 1;
      log("Season complete! Your county club survived the challenge.");
    } else {
      state.day += 1;
    }

    updateStats();
  }

  function setupActions() {
    runDayButton.addEventListener("click", runDay);
    maintenanceButton.addEventListener("click", function () {
      if (!spend(120, "court maintenance")) {
        return;
      }
      state.courtCondition = clamp(state.courtCondition + 14, 0, 100);
      state.happiness = clamp(state.happiness + 3, 0, 100);
      log("Maintenance complete. Courts are in better shape.");
      updateStats();
    });
    marketingButton.addEventListener("click", function () {
      if (!spend(150, "marketing push")) {
        return;
      }
      state.reputation = clamp(state.reputation + 8, 0, 100);
      state.happiness = clamp(state.happiness + 2, 0, 100);
      log("Marketing campaign launched. Interest in the club is rising.");
      updateStats();
    });
    buildButton.addEventListener("click", function () {
      if (!spend(700, "new court")) {
        return;
      }
      state.courts += 1;
      state.reputation = clamp(state.reputation + 4, 0, 100);
      log("Construction done. You opened an additional court.");
      updateStats();
    });
    tournamentButton.addEventListener("click", function () {
      if (!spend(220, "junior tournament")) {
        return;
      }
      state.reputation = clamp(state.reputation + 6, 0, 100);
      state.happiness = clamp(state.happiness + 7, 0, 100);
      state.members = clamp(state.members + randomInt(1, 3), 25, 350);
      log("Tournament day was a success and brought new energy to the club.");
      updateStats();
    });
    restartButton.addEventListener("click", function () {
      state = createInitialState();
      logNode.innerHTML = "";
      log("New county club season started.");
      updateStats();
    });
  }

  state = createInitialState();
  setupActions();
  log("Welcome manager! Keep the county club thriving.");
  updateStats();
})();
