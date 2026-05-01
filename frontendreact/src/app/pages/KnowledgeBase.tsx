import { BookOpen, Search, Star, Clock, TrendingUp } from 'lucide-react';

const categories = [
  { name: 'Product Information', count: 145, icon: '📦' },
  { name: 'Clinical Studies', count: 89, icon: '🔬' },
  { name: 'Training Materials', count: 234, icon: '📚' },
  { name: 'Compliance Guidelines', count: 67, icon: '✅' },
  { name: 'Best Practices', count: 156, icon: '⭐' },
  { name: 'FAQs', count: 203, icon: '❓' },
];

const recentArticles = [
  {
    title: 'Understanding New Product Efficacy Data',
    category: 'Clinical Studies',
    views: 342,
    updated: '2 days ago',
    rating: 4.8,
  },
  {
    title: 'Best Practices for Objection Handling',
    category: 'Best Practices',
    views: 567,
    updated: '1 week ago',
    rating: 4.9,
  },
  {
    title: 'Compliance Training Module 2026',
    category: 'Compliance Guidelines',
    views: 289,
    updated: '3 days ago',
    rating: 4.7,
  },
  {
    title: 'Advanced Communication Techniques',
    category: 'Training Materials',
    views: 423,
    updated: '5 days ago',
    rating: 4.8,
  },
];

export function KnowledgeBase() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-slate-900 mb-2">Knowledge Base</h1>
            <p className="text-slate-600">Access training materials, guidelines, and resources</p>
          </div>
          <button className="px-6 py-3 rounded-lg bg-gradient-to-r from-blue-600 to-teal-500 text-white font-medium shadow-lg hover:shadow-xl transition-all">
            Add New Article
          </button>
        </div>
      </div>

      {/* Search Bar */}
      <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="text"
            placeholder="Search knowledge base..."
            className="w-full pl-12 pr-4 py-3 rounded-lg bg-slate-100 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all"
          />
        </div>
      </div>

      {/* Categories Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {categories.map((category, index) => (
          <div
            key={index}
            className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 cursor-pointer"
          >
            <div className="flex items-center gap-3 mb-3">
              <span className="text-3xl">{category.icon}</span>
              <div>
                <h3 className="font-semibold text-slate-900">{category.name}</h3>
                <p className="text-sm text-slate-500">{category.count} articles</p>
              </div>
            </div>
            <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
              Browse →
            </button>
          </div>
        ))}
      </div>

      {/* Recent Articles */}
      <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-semibold text-slate-900">Recent Articles</h3>
          <button className="text-sm text-blue-600 hover:text-blue-700">View All</button>
        </div>

        <div className="space-y-4">
          {recentArticles.map((article, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-4 rounded-lg bg-slate-50 hover:bg-slate-100 transition-colors cursor-pointer"
            >
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-600 to-teal-500 flex items-center justify-center">
                  <BookOpen className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h4 className="font-medium text-slate-900 mb-1">{article.title}</h4>
                  <div className="flex items-center gap-3 text-sm text-slate-500">
                    <span>{article.category}</span>
                    <span>•</span>
                    <span className="flex items-center gap-1">
                      <TrendingUp className="w-3 h-3" />
                      {article.views} views
                    </span>
                    <span>•</span>
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {article.updated}
                    </span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                <span className="text-sm font-medium text-slate-900">{article.rating}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Links */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-blue-600 to-blue-500 rounded-2xl p-6 text-white shadow-lg cursor-pointer hover:shadow-xl transition-all">
          <h3 className="text-lg font-semibold mb-2">Video Tutorials</h3>
          <p className="text-blue-100 text-sm mb-4">Watch step-by-step guides</p>
          <p className="text-2xl font-bold">48 videos</p>
        </div>

        <div className="bg-gradient-to-br from-teal-600 to-teal-500 rounded-2xl p-6 text-white shadow-lg cursor-pointer hover:shadow-xl transition-all">
          <h3 className="text-lg font-semibold mb-2">Downloads</h3>
          <p className="text-teal-100 text-sm mb-4">PDF guides and resources</p>
          <p className="text-2xl font-bold">156 files</p>
        </div>

        <div className="bg-gradient-to-br from-purple-600 to-purple-500 rounded-2xl p-6 text-white shadow-lg cursor-pointer hover:shadow-xl transition-all">
          <h3 className="text-lg font-semibold mb-2">Contact Support</h3>
          <p className="text-purple-100 text-sm mb-4">Get help from our team</p>
          <p className="text-2xl font-bold">24/7</p>
        </div>
      </div>
    </div>
  );
}
