const fs = require('fs');
const path = require('path');
const https = require('https');

const FEC_API_KEY = process.env.FEC_API_KEY;
const CYCLE = 2024;
const OUTPUT_DIR = 'data/donors';

function fetchTopDonors(committeeId, candidateName) {
  return new Promise((resolve, reject) => {
    const url = `https://api.fec.gov/v1/schedules/schedule_a/?api_key=${FEC_API_KEY}&committee_id=${committeeId}&two_year_transaction_period=${CYCLE}&sort=-contribution_receipt_amount&per_page=10`;

    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const result = JSON.parse(data);
        const donors = result.results.map(d => ({
          name: d.contributor_name,
          amount: d.contribution_receipt_amount
        }));
        const filename = candidateName.replace(/\s+/g, '_').toLowerCase() + '.json';
        fs.writeFileSync(path.join(OUTPUT_DIR, filename), JSON.stringify(donors, null, 2));
        console.log(`✅ Donors saved for ${candidateName}`);
        resolve();
      });
    }).on('error', reject);
  });
}

function main() {
  if (!fs.existsSync('data/house_members.json')) return console.error("Missing house_members.json");
  if (!fs.existsSync('data/senate_members.json')) return console.error("Missing senate_members.json");

  const allMembers = [
    ...JSON.parse(fs.readFileSync('data/house_members.json')),
    ...JSON.parse(fs.readFileSync('data/senate_members.json')),
  ];

  if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  const promises = allMembers.map(member => {
    const committeeId = member?.principal_committees?.[0]?.committee_id;
    if (!committeeId) return Promise.resolve();
    return fetchTopDonors(committeeId, member.name);
  });

  Promise.all(promises)
    .then(() => console.log("✅ All donor data fetched."))
    .catch(console.error);
}

main();
